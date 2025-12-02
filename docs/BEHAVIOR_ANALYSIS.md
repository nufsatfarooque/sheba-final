# Customer Behavior Analysis Feature

## Overview

A comprehensive customer behavior analysis system that uses **generalized dataset framework**, **RFM analysis**, **ML-based churn prediction**, and **uplift modeling** to provide actionable customer insights and personalized intervention recommendations.

## Key Features

### 1. **Generalized Dataset Ingestion**
- ✅ Supports 4 real-world dataset formats:
  - **Criteo** (Advertising/Marketing)
  - **Hillstrom** (Email Marketing)
  - **Financial Services** (Banking/FinTech)
  - **B2B SaaS** (Enterprise Software)
- ✅ Automatic schema normalization to universal RFM framework
- ✅ Unit conversion and edge case handling
- ✅ CSV upload with progress tracking

### 2. **Churn Risk & Customer Behavior Analysis**
- ✅ RFM-based churn scoring (Recency, Frequency, Monetary)
- ✅ Hybrid ML ensemble (Random Forest + Gradient Boosting)
- ✅ Customer segmentation (Champions, At Risk, Lost, etc.)
- ✅ Behavior summaries with insights and trends
- ✅ Risk indicators and warning signals

### 3. **Uplift Modeling & Intervention Optimization**
- ✅ X-Learner for treatment effect prediction
- ✅ Customer type classification:
  - **Persuadables**: Will respond to treatment
  - **Sure Things**: Will stay anyway
  - **Lost Causes**: Won't respond to treatment
  - **Sleeping Dogs**: Treatment INCREASES churn risk
- ✅ ROI-optimized intervention recommendations
- ✅ Budget-constrained allocation

### 4. **Industry-Specific Recommendations**
- ✅ E-commerce: Discounts, product recommendations
- ✅ Financial: Fee waivers, relationship manager calls
- ✅ SaaS: Plan downgrades, technical support
- ✅ Telecom: Data boosts, priority support

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  STEP 1: DATA INGESTION                             │
│  - CSV Upload                                       │
│  - Schema Detection & Normalization                │
│  - Universal RFM Mapping                            │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│  STEP 2: FEATURE ENGINEERING                        │
│  - RFM Score Calculation                            │
│  - Behavioral Metrics                               │
│  - Engagement Trends                                │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│  STEP 3: MODEL TRAINING                             │
│  - Churn Prediction (RF + GB Ensemble)              │
│  - Uplift Modeling (X-Learner)                      │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│  STEP 4: BEHAVIOR ANALYSIS                          │
│  - Customer Segmentation                            │
│  - Risk Assessment                                  │
│  - Trend Analysis                                   │
│  - Summary Generation                               │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│  STEP 5: INTERVENTION OPTIMIZATION                  │
│  - Treatment Effect Prediction                      │
│  - ROI Calculation                                  │
│  - Budget Optimization                              │
│  - Personalized Recommendations                     │
└─────────────────────────────────────────────────────┘
```

## Installation

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
pip install -r requirements_behavior_analysis.txt
```

### 2. Run Database Migration

```bash
cd backend
alembic upgrade head
```

This creates the following tables:
- `datasets` - Dataset metadata
- `customers` - Normalized customer records
- `customer_behavior_summaries` - Behavior analysis results
- `interventions` - Intervention recommendations

### 3. Start Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload --port 5000
```

### 4. Start Frontend (Optional)

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### Dataset Management

#### Upload Dataset
```http
POST /api/v1/behavior/upload-data
Content-Type: multipart/form-data

Fields:
- file: CSV file
- dataset_name: string
- dataset_type: "criteo" | "hillstrom" | "financial" | "b2b"
- auto_train: boolean (default: true)

Response:
{
  "dataset_id": "uuid",
  "status": "processing",
  "message": "Dataset uploaded successfully"
}
```

#### Get Dataset Status
```http
GET /api/v1/behavior/data/status/{dataset_id}

Response:
{
  "dataset_id": "uuid",
  "name": "Q4 2024 Customer Data",
  "status": "completed",
  "total_records": 50000,
  "treatment_count": 15000,
  "control_count": 35000,
  "churn_rate_treatment": 0.13,
  "churn_rate_control": 0.25,
  "created_at": "2024-12-02T10:00:00Z",
  "completed_at": "2024-12-02T10:15:00Z"
}
```

#### List All Datasets
```http
GET /api/v1/behavior/datasets

Response: Array of dataset status objects
```

### Churn Risk Analysis

#### Get Churn Risk Scores
```http
POST /api/v1/behavior/customers/churn-risk?dataset_id={dataset_id}

Body:
{
  "customer_ids": ["C001", "C002"],  // Optional
  "segment": "At Risk",               // Optional
  "min_risk_score": 50,               // Optional
  "max_risk_score": 100,              // Optional
  "limit": 100
}

Response:
{
  "results": [
    {
      "customer_id": "C001",
      "churn_risk_score": 78.5,
      "risk_level": "High",
      "segment": "At Risk",
      "uplift_score": 0.42,
      "clv_estimate": 2500.00
    }
  ],
  "total_count": 1523,
  "status": "success"
}
```

### Customer Behavior Analysis

#### Get Customer Behavior Summary
```http
GET /api/v1/behavior/customers/{customer_id}/behavior?dataset_id={dataset_id}

Response:
{
  "customer_id": "C001",
  "churn_risk_score": 78.5,
  "segment": "At Risk",
  "customer_type": "Persuadable",
  "profile": {
    "segment": "At Risk",
    "tenure": "365 days (12 months)",
    "lifecycle_stage": "Mature",
    "customer_type": "Moderately Engaged"
  },
  "engagement": {
    "activity_level": "Moderate",
    "last_active": "45 days ago",
    "avg_frequency": "5.2 activities/month",
    "engagement_score": "62.5/100",
    "engagement_trend": "Decreasing ↘",
    "session_activity": "15 sessions/month"
  },
  "value": {
    "total_value_90d": "$450.00",
    "total_value_30d": "$120.00",
    "avg_transaction": "$28.50",
    "value_segment": "Medium Value",
    "monthly_average": "$120.00/month"
  },
  "insights": {
    "trends": [
      "⚠️ Declining activity over recent period",
      "💰 High-value but disengaging"
    ],
    "risk_indicators": [
      {
        "type": "Critical",
        "indicator": "Very high churn probability",
        "action": "Immediate intervention required",
        "priority": "High"
      }
    ]
  },
  "recommendations": [
    {
      "priority": "Critical",
      "action": "Personal outreach from account manager",
      "reason": "Critical churn risk detected",
      "expected_impact": "High",
      "timing": "Immediate"
    },
    {
      "priority": "Critical",
      "action": "Offer retention incentive (15-20% value)",
      "reason": "Prevent imminent churn of valuable customer",
      "expected_impact": "High",
      "timing": "Within 24 hours"
    }
  ],
  "generated_at": "2024-12-02T10:30:00Z"
}
```

### Intervention Recommendations

#### Get Intervention Recommendations
```http
POST /api/v1/behavior/interventions/recommend?dataset_id={dataset_id}

Body:
{
  "customer_ids": ["C001", "C002"],   // Optional
  "min_uplift_threshold": 0.1,
  "budget": 10000.00,                 // Optional
  "max_interventions": 100,           // Optional
  "industry": "ecommerce"
}

Response:
{
  "interventions": [
    {
      "customer_id": "C001",
      "treatment_id": "discount_15pct",
      "intervention_type": "discount",
      "channel": "in_app",
      "uplift_score": 0.68,
      "expected_value": 1700.00,
      "roi": 467.0,
      "cost": 300.00,
      "message_body": "As a valued customer, get 15% off",
      "recommended_timing": "immediate"
    }
  ],
  "total_recommended": 25,
  "total_budget_allocated": 7500.00,
  "expected_total_value": 42500.00,
  "status": "success"
}
```

### Dataset Statistics

#### Get Aggregated Statistics
```http
GET /api/v1/behavior/datasets/{dataset_id}/stats

Response:
{
  "dataset_id": "uuid",
  "total_customers": 50000,
  "segments": {
    "Champions": 5000,
    "Loyal Customers": 8000,
    "At Risk": 12000,
    "Lost/Hibernating": 3000,
    "New Customers": 10000,
    "Need Attention": 12000
  },
  "risk_levels": {
    "Critical": 3000,
    "High": 12000,
    "Medium": 20000,
    "Low": 15000
  },
  "avg_churn_risk": 45.2,
  "avg_clv": 1250.00,
  "treatment_effect": 0.12
}
```

## Dataset Formats

### 1. Criteo Dataset

**Required Columns:**
- `f0-f11`: 12 anonymized features (continuous)
- `treatment`: {0, 1} - Treatment flag
- `exposure`: {0, 1} - Ad exposure
- `visit`: {0, 1} - Website visit
- `conversion`: {0, 1} - Purchase (outcome)

**Download:** [Criteo Uplift Modeling Dataset](https://ailab.criteo.com/criteo-uplift-prediction-dataset/)

### 2. Hillstrom Email Marketing Dataset

**Required Columns:**
- `recency`: Months since last purchase
- `history`: Total spend in past 12 months
- `mens`: {0, 1} - Received men's email
- `womens`: {0, 1} - Received women's email
- `zip_code`: Geographic info
- `newbie`: {0, 1} - New vs returning
- `channel`: Phone/Web/Multichannel
- `visit`: {0, 1} - Visited within 2 weeks
- `conversion`: {0, 1} - Made purchase
- `spend`: Amount spent

**Download:** [Hillstrom Dataset](https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html)

### 3. Financial Services Dataset

**Required/Recommended Columns:**
- `customer_id`
- `treatment`: {0, 1} - Retention campaign target
- `churned`: {0, 1} - Churned
- `age`, `gender`
- `account_balance`
- `transaction_count_30d`, `transaction_count_90d`
- `avg_transaction_value`
- `products_owned`
- `tenure_months`
- `last_login_days`
- `support_tickets_90d`
- `credit_score` (optional)

### 4. B2B SaaS Dataset

**Required/Recommended Columns:**
- `customer_id`
- `treatment`: {0, 1} - Retention call
- `churned`: {0, 1} - Canceled subscription
- `contract_value_per_month`
- `contract_duration_months`
- `feature_usage_count`
- `support_tickets`
- `user_seats`, `seats_active`
- `industry`, `company_size`
- `days_since_last_login`

## Schema Normalization

All datasets are normalized to a **Universal RFM Schema**:

### Universal Schema Fields

```python
{
    # Identity
    "customer_id": str,

    # Treatment & Outcome
    "treatment": int,           # 0 or 1
    "treatment_type": str,
    "outcome": int,             # 0 = retained, 1 = churned

    # RECENCY
    "days_since_last_activity": float,
    "recency_score": int,       # 1-5 (5 = best)

    # FREQUENCY
    "activity_count_30d": int,
    "activity_count_90d": int,
    "frequency_score": int,     # 1-5

    # MONETARY
    "total_value_30d": float,
    "total_value_90d": float,
    "avg_value_per_activity": float,
    "monetary_score": int,      # 1-5

    # COMBINED
    "rfm_score": int,           # 3-15

    # BEHAVIORAL
    "tenure_days": int,
    "engagement_score": float,  # 0-100
    "activity_trend": float,    # % change
    "feature_usage_count": int,
    "session_count_30d": int,

    # SUPPORT
    "support_tickets_30d": int,
    "satisfaction_score": float,

    # FINANCIAL
    "payment_failures": int,
    "account_balance": float
}
```

### Edge Cases Handled

1. **Different Time Units**
   - Seconds, minutes, hours, days, weeks, months
   - Auto-detection based on column name and value ranges
   - Normalized to days

2. **Different Currencies**
   - USD, EUR, GBP, BDT, INR, JPY
   - Normalized to USD
   - (Use forex API in production)

3. **Missing Columns**
   - Intelligent defaults based on available data
   - Derived metrics from related fields

4. **Different Granularities**
   - Daily, weekly, monthly data
   - Aggregated to common timeframe

## Example Usage

### Python/Jupyter Notebook

```python
import requests
import pandas as pd

API_BASE = "http://localhost:5000/api/v1"
TOKEN = "your_auth_token"

headers = {"Authorization": f"Bearer {TOKEN}"}

# Upload dataset
with open("hillstrom_data.csv", "rb") as f:
    files = {"file": f}
    data = {
        "dataset_name": "Q4 2024 Email Campaign",
        "dataset_type": "hillstrom",
        "auto_train": "true"
    }
    response = requests.post(
        f"{API_BASE}/behavior/upload-data",
        files=files,
        data=data,
        headers=headers
    )
    dataset_id = response.json()["dataset_id"]

# Check status
response = requests.get(
    f"{API_BASE}/behavior/data/status/{dataset_id}",
    headers=headers
)
print(response.json())

# Get churn risk for high-risk customers
response = requests.post(
    f"{API_BASE}/behavior/customers/churn-risk?dataset_id={dataset_id}",
    json={"min_risk_score": 70, "limit": 50},
    headers=headers
)
high_risk_customers = response.json()["results"]

# Get intervention recommendations
response = requests.post(
    f"{API_BASE}/behavior/interventions/recommend?dataset_id={dataset_id}",
    json={
        "min_uplift_threshold": 0.15,
        "budget": 10000,
        "industry": "ecommerce"
    },
    headers=headers
)
interventions = response.json()["interventions"]

# Example output:
# Rahima – 78% churn risk → $300 discount + reminder
# Expected retention +68%, ROI 1500%
```

### cURL

```bash
# Upload dataset
curl -X POST http://localhost:5000/api/v1/behavior/upload-data \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@hillstrom_data.csv" \
  -F "dataset_name=Q4 2024 Campaign" \
  -F "dataset_type=hillstrom" \
  -F "auto_train=true"

# Get customer behavior
curl -X GET "http://localhost:5000/api/v1/behavior/customers/C001/behavior?dataset_id=$DATASET_ID" \
  -H "Authorization: Bearer $TOKEN"
```

## Implementation Details

### Churn Risk Scoring

Combines two approaches:

1. **RFM-Based (40% weight)**
   ```python
   engagement = (R*0.4 + F*0.3 + M*0.3)
   churn_risk = 100 - ((engagement - 1) / 4 * 100)
   ```

2. **ML-Based (60% weight)**
   - Random Forest (n_estimators=100)
   - Gradient Boosting (n_estimators=100)
   - Ensemble average

### Uplift Modeling (X-Learner)

**Stage 1:** Train response models
- μ₁(x): Model for treatment group
- μ₀(x): Model for control group

**Stage 2:** Impute treatment effects
- τ₁ = Y₁ - μ₀(X₁) for treatment group
- τ₀ = μ₁(X₀) - Y₀ for control group

**Stage 3:** Train effect models
- E[τ₁|X] and E[τ₀|X]

**Stage 4:** Combine using propensity
- τ(x) = g(x)·E[τ₀|X] + (1-g(x))·E[τ₁|X]
- g(x) = propensity score

### Customer Type Classification

```python
if uplift > 0.1:
    type = "Persuadable"     # Will respond to treatment
elif uplift < -0.1:
    type = "Sleeping Dog"    # Treatment HARMS retention
elif baseline_churn < 0.3:
    type = "Sure Thing"      # Will stay anyway
else:
    type = "Lost Cause"      # Won't respond
```

## Research References

This implementation is based on:

1. **RFM Analysis**: Hughes, A. M. (1994). Strategic Database Marketing
2. **Uplift Modeling**: Radcliffe, N. J., & Surry, P. D. (2011). Real-World Uplift Modelling
3. **X-Learner**: Künzel, S. R., et al. (2019). Metalearners for estimating heterogeneous treatment effects
4. **Causal Inference**: Rubin, D. B. (1974). Causal inference using potential outcomes

## Performance Benchmarks

- **Dataset Processing**: ~1000 records/second
- **Model Training**: ~5 minutes for 50K customers
- **Prediction**: ~10,000 customers/second
- **API Response Time**: <200ms for single customer

## Troubleshooting

### Dataset Upload Fails

```bash
# Check file size limit (default 100MB)
# Increase in nginx/gunicorn config

# Check CSV encoding
# Use UTF-8 encoding
```

### Models Not Training

```bash
# Check minimum data requirements:
# - At least 1,000 customers
# - At least 100 in treatment group
# - At least 100 in control group
```

### Low Uplift Scores

```python
# Check data quality:
# 1. Is there actual treatment effect in data?
# 2. Are treatment and control groups balanced?
# 3. Check for data leakage
```

## Future Enhancements

- [ ] Survival analysis (Cox Proportional Hazards)
- [ ] SHAP values for model explainability
- [ ] Real-time scoring API
- [ ] A/B test framework
- [ ] Automated model retraining
- [ ] Multi-armed bandit for intervention selection
- [ ] Customer journey mapping
- [ ] Cohort analysis

## License

MIT License

## Support

For issues and questions, please create an issue in the GitHub repository.
