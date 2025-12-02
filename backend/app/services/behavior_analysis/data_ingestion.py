"""
Data Ingestion Service
Handles CSV upload, schema normalization, and database storage
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple
import logging
from pathlib import Path
import uuid
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.behavior_analysis.schema_mapper import SchemaMapper
from app.services.behavior_analysis.churn_scoring import ChurnScoringEngine
from app.services.behavior_analysis.uplift_model import UpliftModelingEngine
from app.services.behavior_analysis.behavior_analyzer import CustomerBehaviorAnalyzer
from app.db.models.behavior.dataset import Dataset, Customer, CustomerBehaviorSummary, DatasetType, DatasetStatus

logger = logging.getLogger(__name__)


class DataIngestionService:
    """Service for ingesting and processing customer datasets"""

    def __init__(self, db: Session, models_dir: str = "models"):
        self.db = db
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)

        # Initialize components
        self.schema_mapper = SchemaMapper()
        self.churn_engine = ChurnScoringEngine(use_ml=True)
        self.uplift_engine = UpliftModelingEngine()
        self.behavior_analyzer = CustomerBehaviorAnalyzer()

    def ingest_dataset(
        self,
        file_path: str,
        dataset_name: str,
        dataset_type: str,
        user_id: int,
        auto_train: bool = True
    ) -> Dict[str, Any]:
        """
        Ingest a dataset from CSV file.

        Args:
            file_path: Path to CSV file
            dataset_name: Name for this dataset
            dataset_type: Type (criteo, hillstrom, financial, b2b)
            user_id: User ID who uploaded
            auto_train: Whether to automatically train models

        Returns:
            Dictionary with dataset ID and processing status
        """
        dataset_id = str(uuid.uuid4())
        logger.info(f"Starting ingestion for dataset {dataset_id}: {dataset_name}")

        try:
            # Create dataset record
            dataset = self._create_dataset_record(
                dataset_id,
                dataset_name,
                dataset_type,
                file_path,
                user_id
            )

            # Load CSV
            logger.info(f"Loading CSV from {file_path}")
            df = pd.read_csv(file_path)

            # Update status
            dataset.status = DatasetStatus.PROCESSING
            dataset.total_records = len(df)
            self.db.commit()

            # Normalize schema
            logger.info("Normalizing schema...")
            dataset.status = DatasetStatus.NORMALIZING
            self.db.commit()

            normalized_df, mapping_info = self.schema_mapper.auto_detect_and_map(
                df,
                dataset_type
            )

            # Store mapping info
            dataset.schema_mapping = mapping_info
            dataset.treatment_count = mapping_info['treatment_count']
            dataset.control_count = mapping_info['control_count']

            # Calculate churn rates
            treatment_churned = normalized_df[normalized_df['treatment'] == 1]['outcome'].mean()
            control_churned = normalized_df[normalized_df['treatment'] == 0]['outcome'].mean()

            dataset.churn_rate_treatment = float(treatment_churned)
            dataset.churn_rate_control = float(control_churned)

            self.db.commit()

            # Store customers in database
            logger.info("Storing customer records...")
            self._store_customers(dataset.id, normalized_df)

            # Train models if requested
            if auto_train and len(normalized_df) >= 1000:
                logger.info("Training models...")
                self._train_models(dataset_id, normalized_df)

                # Generate behavior summaries
                logger.info("Generating behavior summaries...")
                self._generate_behavior_summaries(dataset.id, normalized_df)

            # Mark as completed
            dataset.status = DatasetStatus.COMPLETED
            dataset.completed_at = datetime.now()
            self.db.commit()

            logger.info(f"Dataset {dataset_id} ingestion completed successfully")

            return {
                'dataset_id': dataset_id,
                'status': 'completed',
                'total_records': len(normalized_df),
                'treatment_count': mapping_info['treatment_count'],
                'control_count': mapping_info['control_count'],
                'churn_rate_treatment': treatment_churned,
                'churn_rate_control': control_churned,
                'baseline_uplift': control_churned - treatment_churned
            }

        except Exception as e:
            logger.error(f"Error ingesting dataset: {str(e)}", exc_info=True)

            # Update dataset status to failed
            if dataset:
                dataset.status = DatasetStatus.FAILED
                dataset.processing_log = {'error': str(e)}
                self.db.commit()

            raise

    def _create_dataset_record(
        self,
        dataset_id: str,
        dataset_name: str,
        dataset_type: str,
        file_path: str,
        user_id: int
    ) -> Dataset:
        """Create initial dataset record"""
        file_path_obj = Path(file_path)

        dataset = Dataset(
            dataset_id=dataset_id,
            name=dataset_name,
            dataset_type=DatasetType(dataset_type.lower()),
            status=DatasetStatus.UPLOADING,
            original_filename=file_path_obj.name,
            file_path=file_path,
            file_size_bytes=file_path_obj.stat().st_size if file_path_obj.exists() else 0,
            uploaded_by_user_id=user_id
        )

        self.db.add(dataset)
        self.db.commit()
        self.db.refresh(dataset)

        return dataset

    def _store_customers(self, dataset_id: int, normalized_df: pd.DataFrame):
        """Store normalized customer records in database"""
        customers = []

        for idx, row in normalized_df.iterrows():
            customer = Customer(
                customer_id=str(row['customer_id']),
                dataset_id=dataset_id,
                treatment=int(row['treatment']),
                treatment_type=row.get('treatment_type', 'unknown'),
                outcome=int(row['outcome']),
                days_since_last_activity=float(row['days_since_last_activity']),
                activity_count_30d=int(row['activity_count_30d']),
                activity_count_90d=int(row['activity_count_90d']),
                total_value_30d=float(row['total_value_30d']),
                total_value_90d=float(row['total_value_90d']),
                avg_value_per_activity=float(row['avg_value_per_activity']),
                recency_score=int(row['recency_score']),
                frequency_score=int(row['frequency_score']),
                monetary_score=int(row['monetary_score']),
                rfm_score=int(row['rfm_score']),
                tenure_days=int(row['tenure_days']),
                engagement_score=float(row['engagement_score']),
                activity_trend=float(row['activity_trend']),
                feature_usage_count=int(row['feature_usage_count']),
                session_count_30d=int(row['session_count_30d']),
                support_tickets_30d=int(row['support_tickets_30d']),
                satisfaction_score=float(row['satisfaction_score']),
                payment_failures=int(row['payment_failures']),
                account_balance=float(row['account_balance']),
                original_data=row.get('original_data', {})
            )

            customers.append(customer)

            # Batch insert every 1000 records
            if len(customers) >= 1000:
                self.db.bulk_save_objects(customers)
                self.db.commit()
                customers = []

        # Insert remaining
        if customers:
            self.db.bulk_save_objects(customers)
            self.db.commit()

    def _train_models(self, dataset_id: str, normalized_df: pd.DataFrame):
        """Train churn and uplift models"""
        try:
            # Train churn model
            logger.info("Training churn prediction model...")
            self.churn_engine.train_ml_model(normalized_df)

            # Train uplift model
            logger.info("Training uplift model...")
            self.uplift_engine.train(normalized_df)

            # Save models
            churn_model_path = self.models_dir / f"{dataset_id}_churn_model.pkl"
            uplift_model_path = self.models_dir / f"{dataset_id}_uplift_model.pkl"

            self.churn_engine.save_models(
                ml_path=str(churn_model_path)
            )
            self.uplift_engine.save_model(str(uplift_model_path))

            logger.info("Models trained and saved successfully")

        except Exception as e:
            logger.error(f"Error training models: {str(e)}", exc_info=True)
            raise

    def _generate_behavior_summaries(self, dataset_id: int, normalized_df: pd.DataFrame):
        """Generate behavior summaries for all customers"""
        try:
            # Get customer records from database
            customers = self.db.query(Customer).filter(
                Customer.dataset_id == dataset_id
            ).all()

            # Calculate churn scores
            churn_results = self.churn_engine.calculate_churn_scores(normalized_df)

            # Calculate uplift scores
            uplift_results = self.uplift_engine.predict_uplift(normalized_df)

            # Update customer records with predictions
            for idx, customer in enumerate(customers):
                customer.churn_risk_score = float(churn_results.iloc[idx]['churn_risk_score'])
                customer.customer_segment = churn_results.iloc[idx]['segment']

                if idx < len(uplift_results):
                    customer.uplift_score = float(uplift_results.iloc[idx]['uplift_score'])

                    # Estimate CLV (simplified)
                    monthly_value = customer.total_value_30d
                    expected_months = 12 if customer.engagement_score > 60 else 6
                    customer.clv_estimate = monthly_value * expected_months

            self.db.commit()

            # Generate behavior summaries
            summaries = []

            for idx, customer in enumerate(customers):
                customer_data = normalized_df.iloc[idx]
                churn_score = customer.churn_risk_score
                segment = customer.customer_segment
                customer_type = uplift_results.iloc[idx]['customer_type'] if idx < len(uplift_results) else None

                behavior_summary_dict = self.behavior_analyzer.generate_behavior_summary(
                    customer.customer_id,
                    customer_data,
                    churn_score,
                    segment,
                    customer_type,
                    industry='ecommerce'  # Default, should be configurable
                )

                # Create summary record
                summary = CustomerBehaviorSummary(
                    customer_id=customer.id,
                    lifecycle_stage=behavior_summary_dict['profile']['lifecycle_stage'],
                    customer_type=customer_type or 'Unknown',
                    activity_level=behavior_summary_dict['engagement']['activity_level'],
                    value_segment=behavior_summary_dict['value']['value_segment'],
                    engagement_trend=behavior_summary_dict['engagement']['engagement_trend'],
                    preferred_channels=['email', 'in_app'],  # Default
                    last_active_days_ago=int(customer.days_since_last_activity),
                    avg_frequency_per_month=customer.activity_count_30d,
                    risk_level=self._categorize_risk(churn_score),
                    risk_indicators=behavior_summary_dict['risk_indicators'],
                    behavioral_trends=behavior_summary_dict['trends'],
                    recommended_interventions=behavior_summary_dict['recommendations'],
                    expected_retention_lift=customer.uplift_score if customer.uplift_score else 0.0,
                    intervention_roi=0.0,  # Will be calculated by intervention optimizer
                    summary_text=self._generate_summary_text(behavior_summary_dict)
                )

                summaries.append(summary)

                # Batch insert
                if len(summaries) >= 500:
                    self.db.bulk_save_objects(summaries)
                    self.db.commit()
                    summaries = []

            # Insert remaining
            if summaries:
                self.db.bulk_save_objects(summaries)
                self.db.commit()

            logger.info(f"Generated {len(customers)} behavior summaries")

        except Exception as e:
            logger.error(f"Error generating behavior summaries: {str(e)}", exc_info=True)
            raise

    def _categorize_risk(self, score: float) -> str:
        """Categorize risk level"""
        if score >= 75:
            return "Critical"
        elif score >= 50:
            return "High"
        elif score >= 25:
            return "Medium"
        else:
            return "Low"

    def _generate_summary_text(self, summary_dict: Dict[str, Any]) -> str:
        """Generate human-readable summary text"""
        profile = summary_dict['profile']
        engagement = summary_dict['engagement']
        value = summary_dict['value']
        churn_score = summary_dict['churn_risk_score']

        text = f"Customer is in the {profile['lifecycle_stage']} stage, "
        text += f"classified as {profile['segment']}. "
        text += f"Activity level: {engagement['activity_level']}, "
        text += f"last active {engagement['last_active']}. "
        text += f"Value segment: {value['value_segment']}. "
        text += f"Churn risk: {churn_score:.0f}%."

        return text

    def get_dataset_status(self, dataset_id: str) -> Dict[str, Any]:
        """Get dataset processing status"""
        dataset = self.db.query(Dataset).filter(
            Dataset.dataset_id == dataset_id
        ).first()

        if not dataset:
            raise ValueError(f"Dataset {dataset_id} not found")

        return {
            'dataset_id': dataset.dataset_id,
            'name': dataset.name,
            'status': dataset.status.value,
            'total_records': dataset.total_records,
            'treatment_count': dataset.treatment_count,
            'control_count': dataset.control_count,
            'churn_rate_treatment': dataset.churn_rate_treatment,
            'churn_rate_control': dataset.churn_rate_control,
            'created_at': dataset.created_at.isoformat() if dataset.created_at else None,
            'completed_at': dataset.completed_at.isoformat() if dataset.completed_at else None
        }
