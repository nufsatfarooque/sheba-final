"""
API Endpoints for Customer Behavior Analysis
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from pathlib import Path
import uuid
import shutil

from app.api.deps import get_db, get_current_user
from app.schemas.behavior import *
from app.db.models.user import User
from app.db.models.behavior.dataset import Dataset, BehaviorCustomer, CustomerBehaviorSummary
from app.services.behavior_analysis.data_ingestion import DataIngestionService
from app.services.behavior_analysis.churn_scoring import ChurnScoringEngine
from app.services.behavior_analysis.uplift_model import UpliftModelingEngine, InterventionOptimizer
from app.services.behavior_analysis.behavior_analyzer import CustomerBehaviorAnalyzer

router = APIRouter()
logger = logging.getLogger(__name__)

# Directory for uploaded files
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def process_dataset_background(file_path: str, dataset_name: str, dataset_type: str, user_id: int, db: Session):
    """Background task for processing dataset"""
    try:
        ingestion_service = DataIngestionService(db)
        result = ingestion_service.ingest_dataset(
            file_path=file_path,
            dataset_name=dataset_name,
            dataset_type=dataset_type,
            user_id=user_id,
            auto_train=True
        )
        logger.info(f"Dataset processing completed: {result}")
    except Exception as e:
        logger.error(f"Error in background processing: {str(e)}", exc_info=True)


@router.post("/upload-data", response_model=DatasetUploadResponse)
async def upload_dataset(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    dataset_name: str = Form(...),
    dataset_type: DatasetTypeEnum = Form(...),
    auto_train: bool = Form(True),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload and process a customer dataset.

    Supports: Criteo, Hillstrom, Financial Services, B2B datasets

    The dataset will be:
    1. Uploaded and stored
    2. Schema normalized to universal RFM framework
    3. Models trained (churn prediction + uplift modeling)
    4. Behavior summaries generated
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix
        saved_filename = f"{file_id}{file_extension}"
        file_path = UPLOAD_DIR / saved_filename

        # Save uploaded file
        logger.info(f"Saving uploaded file: {file.filename}")
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process in background
        if auto_train:
            background_tasks.add_task(
                process_dataset_background,
                str(file_path),
                dataset_name,
                dataset_type.value,
                current_user.id,
                db
            )

            return DatasetUploadResponse(
                dataset_id=file_id,
                status="processing",
                message=f"Dataset uploaded successfully. Processing in background."
            )
        else:
            # Process immediately
            ingestion_service = DataIngestionService(db)
            result = ingestion_service.ingest_dataset(
                file_path=str(file_path),
                dataset_name=dataset_name,
                dataset_type=dataset_type.value,
                user_id=current_user.id,
                auto_train=False
            )

            return DatasetUploadResponse(
                dataset_id=result['dataset_id'],
                status=result['status'],
                message="Dataset uploaded and processed successfully"
            )

    except Exception as e:
        logger.error(f"Error uploading dataset: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error uploading dataset: {str(e)}")


@router.get("/data/status/{dataset_id}", response_model=DatasetStatusResponse)
async def get_dataset_status(
    dataset_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the processing status of an uploaded dataset.
    """
    dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return DatasetStatusResponse(
        dataset_id=dataset.dataset_id,
        name=dataset.name,
        status=dataset.status.value,
        total_records=dataset.total_records,
        treatment_count=dataset.treatment_count,
        control_count=dataset.control_count,
        churn_rate_treatment=dataset.churn_rate_treatment,
        churn_rate_control=dataset.churn_rate_control,
        created_at=dataset.created_at.isoformat() if dataset.created_at else None,
        completed_at=dataset.completed_at.isoformat() if dataset.completed_at else None
    )


@router.get("/datasets", response_model=List[DatasetStatusResponse])
async def list_datasets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all datasets uploaded by the current user.
    """
    datasets = db.query(Dataset).filter(
        Dataset.uploaded_by_user_id == current_user.id
    ).order_by(Dataset.created_at.desc()).all()

    return [
        DatasetStatusResponse(
            dataset_id=d.dataset_id,
            name=d.name,
            status=d.status.value,
            total_records=d.total_records,
            treatment_count=d.treatment_count,
            control_count=d.control_count,
            churn_rate_treatment=d.churn_rate_treatment,
            churn_rate_control=d.churn_rate_control,
            created_at=d.created_at.isoformat() if d.created_at else None,
            completed_at=d.completed_at.isoformat() if d.completed_at else None
        )
        for d in datasets
    ]


@router.post("/customers/churn-risk", response_model=ChurnRiskResponse)
async def get_churn_risk(
    request: ChurnRiskRequest,
    dataset_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get churn risk scores for customers.

    Filter by:
    - Specific customer IDs
    - Segment
    - Risk score range
    """
    dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Build query
    query = db.query(BehaviorCustomer).filter(BehaviorCustomer.dataset_id == dataset.id)

    if request.customer_ids:
        query = query.filter(BehaviorCustomer.customer_id.in_(request.customer_ids))

    if request.segment:
        query = query.filter(BehaviorCustomer.customer_segment == request.segment)

    if request.min_risk_score is not None:
        query = query.filter(BehaviorCustomer.churn_risk_score >= request.min_risk_score)

    if request.max_risk_score is not None:
        query = query.filter(BehaviorCustomer.churn_risk_score <= request.max_risk_score)

    # Get total count
    total_count = query.count()

    # Apply limit
    customers = query.limit(request.limit).all()

    # Format results
    results = [
        ChurnRiskResult(
            customer_id=c.customer_id,
            churn_risk_score=c.churn_risk_score,
            risk_level=_categorize_risk(c.churn_risk_score),
            segment=c.customer_segment,
            uplift_score=c.uplift_score,
            clv_estimate=c.clv_estimate
        )
        for c in customers
    ]

    return ChurnRiskResponse(
        results=results,
        total_count=total_count,
        status="success"
    )


@router.get("/customers/{customer_id}/behavior", response_model=CustomerBehaviorResponse)
async def get_customer_behavior(
    customer_id: str,
    dataset_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed behavior summary for a specific customer.

    Returns:
    - Profile information
    - Engagement metrics
    - Value analysis
    - Risk indicators
    - Personalized recommendations
    """
    dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    customer = db.query(BehaviorCustomer).filter(
        BehaviorCustomer.dataset_id == dataset.id,
        BehaviorCustomer.customer_id == customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Get behavior summary
    summary = db.query(CustomerBehaviorSummary).filter(
        CustomerBehaviorSummary.customer_id == customer.id
    ).first()

    if not summary:
        raise HTTPException(status_code=404, detail="Behavior summary not generated yet")

    # Format response
    return CustomerBehaviorResponse(
        customer_id=customer.customer_id,
        churn_risk_score=customer.churn_risk_score,
        segment=customer.customer_segment,
        customer_type=summary.customer_type,
        profile=CustomerProfileResponse(
            segment=customer.customer_segment,
            tenure=f"{customer.tenure_days} days",
            lifecycle_stage=summary.lifecycle_stage,
            customer_type=summary.customer_type
        ),
        engagement=CustomerEngagementResponse(
            activity_level=summary.activity_level,
            last_active=f"{summary.last_active_days_ago} days ago",
            avg_frequency=f"{summary.avg_frequency_per_month:.1f} activities/month",
            engagement_score=f"{customer.engagement_score:.1f}/100",
            engagement_trend=summary.engagement_trend,
            session_activity=f"{customer.session_count_30d} sessions/month"
        ),
        value=CustomerValueResponse(
            total_value_90d=f"${customer.total_value_90d:.2f}",
            total_value_30d=f"${customer.total_value_30d:.2f}",
            avg_transaction=f"${customer.avg_value_per_activity:.2f}",
            value_segment=summary.value_segment,
            monthly_average=f"${customer.total_value_30d:.2f}/month"
        ),
        insights={
            'trends': summary.behavioral_trends,
            'risk_indicators': summary.risk_indicators
        },
        recommendations=[
            Recommendation(**rec) for rec in summary.recommended_interventions
        ],
        generated_at=summary.created_at.isoformat() if summary.created_at else None
    )


@router.post("/interventions/recommend", response_model=InterventionResponse)
async def recommend_interventions(
    request: InterventionRequest,
    dataset_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized intervention recommendations with ROI optimization.

    Uses uplift modeling to identify:
    - Persuadables (will respond to treatment)
    - Sure Things (will stay anyway)
    - Lost Causes (won't respond)
    - Sleeping Dogs (treatment harms retention)

    Optimizes under budget constraint.
    """
    dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Get customers
    query = db.query(BehaviorCustomer).filter(BehaviorCustomer.dataset_id == dataset.id)

    if request.customer_ids:
        query = query.filter(BehaviorCustomer.customer_id.in_(request.customer_ids))

    customers = query.all()

    if not customers:
        raise HTTPException(status_code=404, detail="No customers found")

    # Convert to DataFrame for processing
    import pandas as pd

    customer_data = pd.DataFrame([
        {
            'customer_id': c.customer_id,
            'days_since_last_activity': c.days_since_last_activity,
            'activity_count_30d': c.activity_count_30d,
            'activity_count_90d': c.activity_count_90d,
            'total_value_30d': c.total_value_30d,
            'total_value_90d': c.total_value_90d,
            'avg_value_per_activity': c.avg_value_per_activity,
            'recency_score': c.recency_score,
            'frequency_score': c.frequency_score,
            'monetary_score': c.monetary_score,
            'rfm_score': c.rfm_score,
            'tenure_days': c.tenure_days,
            'engagement_score': c.engagement_score,
            'activity_trend': c.activity_trend,
            'feature_usage_count': c.feature_usage_count,
            'session_count_30d': c.session_count_30d,
            'support_tickets_30d': c.support_tickets_30d,
            'satisfaction_score': c.satisfaction_score,
            'payment_failures': c.payment_failures,
            'account_balance': c.account_balance,
            'uplift_score': c.uplift_score or 0,
            'churn_risk_score': c.churn_risk_score
        }
        for c in customers
    ])

    # Create uplift predictions DataFrame
    uplift_predictions = pd.DataFrame({
        'customer_id': customer_data['customer_id'],
        'uplift_score': customer_data['uplift_score'],
        'customer_type': ['Persuadable' if u > 0.1 else 'Other' for u in customer_data['uplift_score']]
    })

    # Get intervention recommendations
    optimizer = InterventionOptimizer()
    recommendations = optimizer.recommend_interventions(
        customer_data=customer_data,
        uplift_predictions=uplift_predictions,
        budget=request.budget,
        min_uplift_threshold=request.min_uplift_threshold,
        max_interventions=request.max_interventions
    )

    if len(recommendations) == 0:
        return InterventionResponse(
            interventions=[],
            total_recommended=0,
            total_budget_allocated=0.0,
            expected_total_value=0.0,
            status="no_interventions_recommended"
        )

    # Format response
    interventions = [
        InterventionRecommendation(
            customer_id=row['customer_id'],
            treatment_id=row['treatment_id'],
            intervention_type=row['intervention_type'],
            channel=row['channel'],
            uplift_score=row['uplift_score'],
            expected_value=row['expected_value'],
            roi=row['roi'],
            cost=row['cost'],
            message_body=row['message_template'],
            recommended_timing=row['recommended_timing']
        )
        for _, row in recommendations.iterrows()
    ]

    return InterventionResponse(
        interventions=interventions,
        total_recommended=len(interventions),
        total_budget_allocated=float(recommendations['cost'].sum()),
        expected_total_value=float(recommendations['expected_value'].sum()),
        status="success"
    )


@router.get("/datasets/{dataset_id}/stats", response_model=DatasetStatsResponse)
async def get_dataset_stats(
    dataset_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get aggregated statistics for a dataset.
    """
    dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    customers = db.query(BehaviorCustomer).filter(BehaviorCustomer.dataset_id == dataset.id).all()

    if not customers:
        raise HTTPException(status_code=404, detail="No customers in dataset")

    # Calculate statistics
    segments = {}
    risk_levels = {}
    total_churn_risk = 0
    total_clv = 0

    for c in customers:
        # Count segments
        segments[c.customer_segment] = segments.get(c.customer_segment, 0) + 1

        # Count risk levels
        risk_level = _categorize_risk(c.churn_risk_score)
        risk_levels[risk_level] = risk_levels.get(risk_level, 0) + 1

        # Sum metrics
        total_churn_risk += c.churn_risk_score
        total_clv += c.clv_estimate or 0

    avg_churn_risk = total_churn_risk / len(customers)
    avg_clv = total_clv / len(customers)

    treatment_effect = (dataset.churn_rate_control or 0) - (dataset.churn_rate_treatment or 0)

    return DatasetStatsResponse(
        dataset_id=dataset.dataset_id,
        total_customers=len(customers),
        segments=segments,
        risk_levels=risk_levels,
        avg_churn_risk=avg_churn_risk,
        avg_clv=avg_clv,
        treatment_effect=treatment_effect
    )


def _categorize_risk(score: float) -> str:
    """Categorize risk level"""
    if score >= 75:
        return "Critical"
    elif score >= 50:
        return "High"
    elif score >= 25:
        return "Medium"
    else:
        return "Low"
