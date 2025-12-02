from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum


class DatasetType(str, enum.Enum):
    CRITEO = "criteo"
    HILLSTROM = "hillstrom"
    FINANCIAL = "financial"
    B2B = "b2b"
    TELCO = "telco"
    CUSTOM = "custom"


class DatasetStatus(str, enum.Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing"
    NORMALIZING = "normalizing"
    COMPLETED = "completed"
    FAILED = "failed"


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    dataset_type = Column(SQLEnum(DatasetType), nullable=False)
    status = Column(SQLEnum(DatasetStatus), default=DatasetStatus.UPLOADING)

    # File information
    original_filename = Column(String)
    file_path = Column(String)
    file_size_bytes = Column(Integer)

    # Statistics
    total_records = Column(Integer)
    treatment_count = Column(Integer)
    control_count = Column(Integer)
    churn_rate_treatment = Column(Float)
    churn_rate_control = Column(Float)

    # Metadata
    schema_mapping = Column(JSON)  # Stores how columns were mapped to universal schema
    processing_log = Column(JSON)  # Stores processing steps and errors

    # User reference
    uploaded_by_user_id = Column(Integer, ForeignKey("users.id"))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    customers = relationship("BehaviorCustomer", back_populates="dataset", cascade="all, delete-orphan")


class BehaviorCustomer(Base):
    __tablename__ = "behavior_customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True, nullable=False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)

    # Treatment and Outcome
    treatment = Column(Integer, nullable=False)  # 0 or 1
    treatment_type = Column(String, nullable=True)  # discount, call, email, etc.
    outcome = Column(Integer, nullable=False)  # 0 = retained, 1 = churned

    # Universal RFM Schema (normalized)
    days_since_last_activity = Column(Float)
    activity_count_30d = Column(Integer)
    activity_count_90d = Column(Integer)
    total_value_30d = Column(Float)
    total_value_90d = Column(Float)
    avg_value_per_activity = Column(Float)
    recency_score = Column(Integer)  # 1-5
    frequency_score = Column(Integer)  # 1-5
    monetary_score = Column(Integer)  # 1-5
    rfm_score = Column(Integer)  # Combined score

    # Behavioral features
    tenure_days = Column(Integer)
    engagement_score = Column(Float)
    activity_trend = Column(Float)  # % change
    feature_usage_count = Column(Integer)
    session_count_30d = Column(Integer)

    # Support/Service
    support_tickets_30d = Column(Integer)
    satisfaction_score = Column(Float)

    # Financial
    payment_failures = Column(Integer)
    account_balance = Column(Float)

    # Predictions (computed after model training)
    churn_risk_score = Column(Float)  # 0-100
    uplift_score = Column(Float)  # Treatment effect
    customer_segment = Column(String)  # Champions, At Risk, etc.
    clv_estimate = Column(Float)  # Customer Lifetime Value

    # Original data (stored as JSON for reference)
    original_data = Column(JSON)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    dataset = relationship("Dataset", back_populates="customers")
    behavior_summary = relationship("CustomerBehaviorSummary", back_populates="customer", uselist=False)
    interventions = relationship("Intervention", back_populates="customer")


class CustomerBehaviorSummary(Base):
    __tablename__ = "customer_behavior_summaries"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("behavior_customers.id"), unique=True, nullable=False)

    # Profile summary
    lifecycle_stage = Column(String)  # New, Growing, Mature, Loyal
    customer_type = Column(String)  # Persuadable, Sure Thing, Lost Cause, Sleeping Dog
    activity_level = Column(String)  # Very Active, Active, Moderate, Low
    value_segment = Column(String)  # High Value, Medium Value, Low Value

    # Engagement analysis
    engagement_trend = Column(String)  # Increasing, Stable, Decreasing
    preferred_channels = Column(JSON)  # List of channels
    last_active_days_ago = Column(Integer)
    avg_frequency_per_month = Column(Float)

    # Risk indicators
    risk_level = Column(String)  # Critical, High, Medium, Low
    risk_indicators = Column(JSON)  # List of risk indicators
    behavioral_trends = Column(JSON)  # List of trends

    # Recommendations
    recommended_interventions = Column(JSON)  # List of recommended actions
    expected_retention_lift = Column(Float)  # Expected improvement from intervention
    intervention_roi = Column(Float)  # Expected ROI

    # Generated summary text
    summary_text = Column(String)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    customer = relationship("BehaviorCustomer", back_populates="behavior_summary")


class Intervention(Base):
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("behavior_customers.id"), nullable=False)

    # Intervention details
    treatment_id = Column(String, nullable=False)  # discount_15pct, vip_support, etc.
    intervention_type = Column(String)  # discount, call, email, etc.
    channel = Column(String)  # in_app, email, phone, sms

    # Scoring
    uplift_score = Column(Float)  # Expected treatment effect
    expected_value = Column(Float)  # Expected financial value
    roi = Column(Float)  # Return on investment
    cost = Column(Float)  # Cost of intervention
    confidence = Column(Float)  # Model confidence

    # Message
    message_title = Column(String)
    message_body = Column(String)
    message_cta = Column(String)  # Call to action

    # Timing
    recommended_timing = Column(String)  # immediate, within_24h, etc.
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    executed_at = Column(DateTime(timezone=True), nullable=True)

    # Status
    status = Column(String, default="recommended")  # recommended, scheduled, executed, failed

    # Results
    customer_responded = Column(Integer, nullable=True)  # 0 or 1
    customer_retained = Column(Integer, nullable=True)  # 0 or 1
    actual_value = Column(Float, nullable=True)

    # Metadata
    widget_config = Column(JSON)  # Widget configuration for in-app interventions
    ab_test_variant = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    customer = relationship("BehaviorCustomer", back_populates="interventions")
