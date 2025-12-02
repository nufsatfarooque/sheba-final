"""
Churn Risk Scoring Engine
Combines RFM-based scoring with ML ensemble models
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, classification_report
import joblib

logger = logging.getLogger(__name__)


class RFMChurnScorer:
    """RFM-based churn risk scoring"""

    def __init__(self, weights: Dict[str, float] = None):
        if weights is None:
            self.weights = {'R': 0.4, 'F': 0.3, 'M': 0.3}
        else:
            self.weights = weights

    def calculate_churn_risk(self, rfm_scores: pd.DataFrame) -> pd.Series:
        """
        Convert RFM scores to churn risk score (0-100).
        Higher score = Higher churn risk
        """
        R = rfm_scores['recency_score'].astype(int)
        F = rfm_scores['frequency_score'].astype(int)
        M = rfm_scores['monetary_score'].astype(int)

        # Calculate engagement score (higher = better customer)
        engagement = (
            R * self.weights['R'] +
            F * self.weights['F'] +
            M * self.weights['M']
        ) / sum(self.weights.values())

        # Invert to get churn risk (lower engagement = higher risk)
        churn_risk = 100 - ((engagement - 1) / 4 * 100)  # Scale 1-5 to 0-100

        return churn_risk

    def segment_customers(self, rfm_scores: pd.DataFrame, churn_risk: pd.Series) -> pd.DataFrame:
        """
        Segment customers based on RFM and churn risk.
        Returns segment name and risk level for each customer.
        """
        segments = []

        for idx in rfm_scores.index:
            row = rfm_scores.loc[idx]
            risk = churn_risk.loc[idx]

            R = row['recency_score']
            F = row['frequency_score']
            M = row['monetary_score']

            # Segmentation logic
            if R >= 4 and F >= 4 and M >= 4:
                segment = "Champions"
                risk_level = "Low"
            elif R >= 4 and F >= 3:
                segment = "Loyal Customers"
                risk_level = "Low"
            elif R >= 4 and F <= 2:
                segment = "New Customers"
                risk_level = "Medium"
            elif R <= 2 and F >= 3:
                segment = "At Risk"
                risk_level = "High"
            elif R <= 2 and F <= 2 and M >= 3:
                segment = "Can't Lose Them"
                risk_level = "Critical"
            elif R <= 2:
                segment = "Lost/Hibernating"
                risk_level = "Critical"
            else:
                segment = "Need Attention"
                risk_level = "Medium"

            segments.append({
                'segment': segment,
                'risk_level': risk_level,
                'churn_risk_score': risk
            })

        return pd.DataFrame(segments, index=rfm_scores.index)


class HybridChurnPredictor:
    """
    Hybrid churn prediction combining RFM + ML models
    """

    def __init__(self):
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        self.gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=5)
        self.scaler = StandardScaler()
        self.rfm_scorer = RFMChurnScorer()
        self.is_fitted = False

        self.feature_columns = [
            'days_since_last_activity',
            'activity_count_30d',
            'activity_count_90d',
            'total_value_30d',
            'total_value_90d',
            'avg_value_per_activity',
            'recency_score',
            'frequency_score',
            'monetary_score',
            'rfm_score',
            'tenure_days',
            'engagement_score',
            'activity_trend',
            'feature_usage_count',
            'session_count_30d',
            'support_tickets_30d',
            'satisfaction_score',
            'payment_failures',
            'account_balance'
        ]

    def engineer_features(self, customer_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create comprehensive feature set combining RFM + behavioral metrics.
        Note: Assumes RFM scores are already calculated
        """
        features = customer_data[self.feature_columns].copy()

        # Additional derived features
        features['inactivity_risk'] = (
            features['days_since_last_activity'] /
            features['tenure_days'].replace(0, 1)
        )

        features['value_per_day'] = (
            features['total_value_90d'] /
            90
        )

        features['activity_decline'] = features['activity_trend'].apply(
            lambda x: 1 if x < -0.2 else 0
        )

        return features

    def train(self, X: pd.DataFrame, y: np.ndarray):
        """
        Train ensemble models.

        Args:
            X: Feature matrix (should include RFM scores)
            y: Target (0 = retained, 1 = churned)
        """
        logger.info("Training hybrid churn prediction models...")

        # Engineer features
        X_engineered = self.engineer_features(X)

        # Scale features
        X_scaled = self.scaler.fit_transform(X_engineered)

        # Train models
        logger.info("Training Random Forest...")
        self.rf_model.fit(X_scaled, y)

        logger.info("Training Gradient Boosting...")
        self.gb_model.fit(X_scaled, y)

        # Calculate and log performance
        train_pred_rf = self.rf_model.predict_proba(X_scaled)[:, 1]
        train_pred_gb = self.gb_model.predict_proba(X_scaled)[:, 1]
        train_pred_ensemble = (train_pred_rf + train_pred_gb) / 2

        train_auc = roc_auc_score(y, train_pred_ensemble)
        logger.info(f"Training AUC: {train_auc:.4f}")

        self.is_fitted = True

    def predict_churn_risk(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict churn risk using model ensemble.

        Returns:
            Churn risk scores (0-100)
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")

        # Engineer features
        X_engineered = self.engineer_features(X)

        # Scale features
        X_scaled = self.scaler.transform(X_engineered)

        # Get predictions from both models
        rf_proba = self.rf_model.predict_proba(X_scaled)[:, 1]
        gb_proba = self.gb_model.predict_proba(X_scaled)[:, 1]

        # Average ensemble
        churn_risk = (rf_proba + gb_proba) / 2 * 100  # Convert to percentage

        return churn_risk

    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance from models"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting feature importance")

        # Get feature names (including engineered ones)
        sample_features = pd.DataFrame(
            np.zeros((1, len(self.feature_columns))),
            columns=self.feature_columns
        )
        engineered = self.engineer_features(sample_features)
        feature_names = engineered.columns.tolist()

        # Combine importance from both models
        rf_importance = self.rf_model.feature_importances_
        gb_importance = self.gb_model.feature_importances_

        importance_df = pd.DataFrame({
            'feature': feature_names,
            'rf_importance': rf_importance,
            'gb_importance': gb_importance,
            'avg_importance': (rf_importance + gb_importance) / 2
        })

        return importance_df.sort_values('avg_importance', ascending=False)

    def save(self, path: str):
        """Save model"""
        model_data = {
            'rf_model': self.rf_model,
            'gb_model': self.gb_model,
            'scaler': self.scaler,
            'rfm_scorer': self.rfm_scorer,
            'is_fitted': self.is_fitted,
            'feature_columns': self.feature_columns
        }
        joblib.dump(model_data, path)
        logger.info(f"Model saved to {path}")

    def load(self, path: str):
        """Load model"""
        model_data = joblib.load(path)
        self.rf_model = model_data['rf_model']
        self.gb_model = model_data['gb_model']
        self.scaler = model_data['scaler']
        self.rfm_scorer = model_data['rfm_scorer']
        self.is_fitted = model_data['is_fitted']
        self.feature_columns = model_data['feature_columns']
        logger.info(f"Model loaded from {path}")


class ChurnScoringEngine:
    """
    Main churn scoring engine.
    Provides both RFM-based and ML-based churn predictions.
    """

    def __init__(self, use_ml: bool = True):
        self.rfm_scorer = RFMChurnScorer()
        self.ml_predictor = HybridChurnPredictor() if use_ml else None
        self.use_ml = use_ml

    def train_ml_model(self, customer_data: pd.DataFrame):
        """Train ML churn prediction model"""
        if not self.use_ml:
            raise ValueError("ML predictor not enabled")

        logger.info("Training ML churn model...")

        # Prepare data
        X = customer_data
        y = customer_data['outcome'].values

        # Train
        self.ml_predictor.train(X, y)

    def calculate_churn_scores(self, customer_data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate churn risk scores using RFM and optionally ML.

        Returns:
            DataFrame with churn scores and segments
        """
        results = pd.DataFrame()
        results['customer_id'] = customer_data['customer_id']

        # RFM-based churn score
        rfm_cols = ['recency_score', 'frequency_score', 'monetary_score']
        rfm_data = customer_data[rfm_cols]

        rfm_churn_risk = self.rfm_scorer.calculate_churn_risk(rfm_data)
        segments_df = self.rfm_scorer.segment_customers(rfm_data, rfm_churn_risk)

        results['rfm_churn_risk'] = rfm_churn_risk.values
        results['segment'] = segments_df['segment'].values
        results['risk_level'] = segments_df['risk_level'].values

        # ML-based churn score (if available)
        if self.use_ml and self.ml_predictor.is_fitted:
            ml_churn_risk = self.ml_predictor.predict_churn_risk(customer_data)
            results['ml_churn_risk'] = ml_churn_risk

            # Combined score (weighted average)
            results['churn_risk_score'] = (
                results['rfm_churn_risk'] * 0.4 +
                results['ml_churn_risk'] * 0.6
            )
        else:
            results['churn_risk_score'] = results['rfm_churn_risk']

        return results

    def save_models(self, rfm_path: str = None, ml_path: str = None):
        """Save trained models"""
        if rfm_path:
            joblib.dump(self.rfm_scorer, rfm_path)

        if ml_path and self.use_ml:
            self.ml_predictor.save(ml_path)

    def load_models(self, rfm_path: str = None, ml_path: str = None):
        """Load trained models"""
        if rfm_path:
            self.rfm_scorer = joblib.load(rfm_path)

        if ml_path and self.use_ml:
            self.ml_predictor.load(ml_path)


def categorize_risk_level(score: float) -> str:
    """Categorize churn risk score into levels"""
    if score >= 75:
        return "Critical"
    elif score >= 50:
        return "High"
    elif score >= 25:
        return "Medium"
    else:
        return "Low"
