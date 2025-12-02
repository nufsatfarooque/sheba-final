"""
Pydantic schemas for behavior analysis API
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class DatasetTypeEnum(str, Enum):
    criteo = "criteo"
    hillstrom = "hillstrom"
    financial = "financial"
    b2b = "b2b"
    telco = "telco"
    custom = "custom"


class DatasetStatusEnum(str, Enum):
    uploading = "uploading"
    processing = "processing"
    normalizing = "normalizing"
    completed = "completed"
    failed = "failed"


class DatasetUploadResponse(BaseModel):
    dataset_id: str
    status: str
    message: str

    class Config:
        from_attributes = True


class DatasetStatusResponse(BaseModel):
    dataset_id: str
    name: str
    status: str
    total_records: Optional[int] = None
    treatment_count: Optional[int] = None
    control_count: Optional[int] = None
    churn_rate_treatment: Optional[float] = None
    churn_rate_control: Optional[float] = None
    created_at: Optional[str] = None
    completed_at: Optional[str] = None

    class Config:
        from_attributes = True


class CustomerProfileResponse(BaseModel):
    segment: str
    tenure: str
    lifecycle_stage: str
    customer_type: str


class CustomerEngagementResponse(BaseModel):
    activity_level: str
    last_active: str
    avg_frequency: str
    engagement_score: str
    engagement_trend: str
    session_activity: str


class CustomerValueResponse(BaseModel):
    total_value_90d: str
    total_value_30d: str
    avg_transaction: str
    value_segment: str
    monthly_average: str


class RiskIndicator(BaseModel):
    type: str
    indicator: str
    action: str
    priority: str


class Recommendation(BaseModel):
    priority: str
    action: str
    reason: str
    expected_impact: Optional[str] = None
    timing: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    channel: Optional[List[str]] = None


class CustomerBehaviorResponse(BaseModel):
    customer_id: str
    churn_risk_score: float
    segment: str
    customer_type: Optional[str] = None
    profile: CustomerProfileResponse
    engagement: CustomerEngagementResponse
    value: CustomerValueResponse
    insights: Dict[str, Any]
    recommendations: List[Recommendation]
    generated_at: str

    class Config:
        from_attributes = True


class ChurnRiskRequest(BaseModel):
    customer_ids: Optional[List[str]] = None
    segment: Optional[str] = None
    min_risk_score: Optional[float] = None
    max_risk_score: Optional[float] = None
    limit: Optional[int] = 100


class ChurnRiskResult(BaseModel):
    customer_id: str
    churn_risk_score: float
    risk_level: str
    segment: str
    uplift_score: Optional[float] = None
    clv_estimate: Optional[float] = None


class ChurnRiskResponse(BaseModel):
    results: List[ChurnRiskResult]
    total_count: int
    status: str


class InterventionRecommendation(BaseModel):
    customer_id: str
    treatment_id: str
    intervention_type: str
    channel: str
    uplift_score: float
    expected_value: float
    roi: float
    cost: float
    confidence: Optional[float] = None
    message_title: Optional[str] = None
    message_body: Optional[str] = None
    message_cta: Optional[str] = None
    recommended_timing: str
    widget_config: Optional[Dict[str, Any]] = None


class InterventionRequest(BaseModel):
    customer_ids: Optional[List[str]] = None
    min_uplift_threshold: float = 0.1
    budget: Optional[float] = None
    max_interventions: Optional[int] = None
    industry: str = 'ecommerce'


class InterventionResponse(BaseModel):
    interventions: List[InterventionRecommendation]
    total_recommended: int
    total_budget_allocated: float
    expected_total_value: float
    status: str


class DatasetStatsResponse(BaseModel):
    dataset_id: str
    total_customers: int
    segments: Dict[str, int]
    risk_levels: Dict[str, int]
    avg_churn_risk: float
    avg_clv: float
    treatment_effect: float


class WidgetTriggerRequest(BaseModel):
    customer_id: str
    current_page: Optional[str] = None
    session_duration: Optional[int] = None


class WidgetResponse(BaseModel):
    show_widget: bool
    widget_type: Optional[str] = None
    message: Optional[str] = None
    options: Optional[List[Dict[str, str]]] = None
    timing: Optional[str] = None


class DataIngestionRequest(BaseModel):
    dataset_name: str = Field(..., description="Name for this dataset")
    dataset_type: DatasetTypeEnum = Field(..., description="Type of dataset")
    auto_train: bool = Field(True, description="Automatically train models after ingestion")


class BatchCustomerRequest(BaseModel):
    dataset_id: str
    customer_ids: Optional[List[str]] = None
    limit: int = 100
    offset: int = 0
