# Quick Start Guide - Customer Behavior Analysis

## Step 1: Install Dependencies

```bash
cd backend

# Install main dependencies
pip install -r requirements.txt

# Install behavior analysis dependencies
pip install -r requirements_behavior_analysis.txt
```

## Step 2: Set Up Database

```bash
# Run migration to create tables
alembic upgrade head
```

This creates the following tables:
- `datasets` - Dataset metadata and processing status
- `customers` - Normalized customer records with RFM scores
- `customer_behavior_summaries` - Behavior analysis and recommendations
- `interventions` - Intervention recommendations with ROI

## Step 3: Generate Sample Data

```bash
# Generate sample datasets
python scripts/generate_sample_data.py
```

This creates 4 sample datasets in `data/sample_datasets/`:
- `criteo_sample.csv` (10,000 records)
- `hillstrom_sample.csv` (10,000 records)
- `financial_sample.csv` (10,000 records)
- `b2b_sample.csv` (5,000 records)

## Step 4: Start Backend Server

```bash
# Start FastAPI server
python -m uvicorn app.main:app --reload --port 5000
```

Server will be available at: http://localhost:5000

API docs: http://localhost:5000/docs

## Step 5: Upload Dataset via API

### Option A: Using cURL

```bash
# Set your auth token
TOKEN="your_auth_token_here"

# Upload Hillstrom dataset
curl -X POST http://localhost:5000/api/v1/behavior/upload-data \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@data/sample_datasets/hillstrom_sample.csv" \
  -F "dataset_name=Hillstrom Email Campaign Q4 2024" \
  -F "dataset_type=hillstrom" \
  -F "auto_train=true"

# Response:
# {
#   "dataset_id": "abc123...",
#   "status": "processing",
#   "message": "Dataset uploaded successfully. Processing in background."
# }
```

### Option B: Using Python

```python
import requests

API_BASE = "http://localhost:5000/api/v1"
TOKEN = "your_auth_token_here"

headers = {"Authorization": f"Bearer {TOKEN}"}

# Upload dataset
with open("data/sample_datasets/hillstrom_sample.csv", "rb") as f:
    files = {"file": f}
    data = {
        "dataset_name": "Hillstrom Email Campaign Q4 2024",
        "dataset_type": "hillstrom",
        "auto_train": "true"
    }
    response = requests.post(
        f"{API_BASE}/behavior/upload-data",
        files=files,
        data=data,
        headers=headers
    )
    result = response.json()
    dataset_id = result["dataset_id"]
    print(f"Dataset ID: {dataset_id}")
```

### Option C: Using Frontend UI

```bash
# In another terminal, start frontend
cd frontend
npm install
npm run dev
```

Navigate to: http://localhost:5173/behavior-analysis

## Step 6: Check Processing Status

```bash
# Get status
curl -X GET "http://localhost:5000/api/v1/behavior/data/status/$DATASET_ID" \
  -H "Authorization: Bearer $TOKEN"

# Response:
# {
#   "dataset_id": "abc123...",
#   "status": "completed",  # or "processing", "normalizing"
#   "total_records": 10000,
#   "treatment_count": 3333,
#   "control_count": 6667,
#   "churn_rate_treatment": 0.15,
#   "churn_rate_control": 0.28,
#   "created_at": "2024-12-02T10:00:00Z",
#   "completed_at": "2024-12-02T10:05:30Z"
# }
```

Processing includes:
1. ✅ CSV upload and validation
2. ✅ Schema normalization to RFM framework
3. ✅ Feature engineering
4. ✅ ML model training (churn + uplift)
5. ✅ Behavior summary generation

Processing time: ~5 minutes for 10K customers

## Step 7: Get Dataset Statistics

```bash
curl -X GET "http://localhost:5000/api/v1/behavior/datasets/$DATASET_ID/stats" \
  -H "Authorization: Bearer $TOKEN"
```

Response:
```json
{
  "dataset_id": "abc123...",
  "total_customers": 10000,
  "segments": {
    "Champions": 1200,
    "Loyal Customers": 1800,
    "At Risk": 2500,
    "Can't Lose Them": 800,
    "Lost/Hibernating": 1500,
    "New Customers": 1400,
    "Need Attention": 800
  },
  "risk_levels": {
    "Critical": 1500,
    "High": 2800,
    "Medium": 3500,
    "Low": 2200
  },
  "avg_churn_risk": 42.5,
  "avg_clv": 1250.00,
  "treatment_effect": 0.13
}
```

## Step 8: Get Customer Behavior Analysis

```bash
# Get behavior summary for a specific customer
curl -X GET "http://localhost:5000/api/v1/behavior/customers/0/behavior?dataset_id=$DATASET_ID" \
  -H "Authorization: Bearer $TOKEN"
```

Response:
```json
{
  "customer_id": "0",
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
    "activity_level": "Low",
    "last_active": "45 days ago",
    "avg_frequency": "3.2 activities/month",
    "engagement_score": "45.8/100",
    "engagement_trend": "Decreasing ↘",
    "session_activity": "9 sessions/month"
  },
  "value": {
    "total_value_90d": "$320.00",
    "total_value_30d": "$85.00",
    "avg_transaction": "$24.50",
    "value_segment": "Medium Value",
    "monthly_average": "$85.00/month"
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
      "priority": "High",
      "action": "Offer retention incentive (15-20% value)",
      "reason": "Prevent imminent churn of valuable customer",
      "expected_impact": "High",
      "timing": "Within 24 hours"
    }
  ]
}
```

## Step 9: Get High-Risk Customers

```bash
# Get customers with churn risk > 70%
curl -X POST "http://localhost:5000/api/v1/behavior/customers/churn-risk?dataset_id=$DATASET_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "min_risk_score": 70,
    "limit": 20
  }'
```

## Step 10: Get Intervention Recommendations

```bash
# Get personalized interventions with ROI optimization
curl -X POST "http://localhost:5000/api/v1/behavior/interventions/recommend?dataset_id=$DATASET_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "min_uplift_threshold": 0.15,
    "budget": 10000,
    "max_interventions": 50,
    "industry": "ecommerce"
  }'
```

Response:
```json
{
  "interventions": [
    {
      "customer_id": "42",
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

**Example Result:**
> Rahima – 78% churn risk → $300 discount + reminder
> Expected retention +68%, ROI 467%

## Understanding the Results

### Customer Types (from Uplift Modeling)

- **Persuadables** (Target These!): Will respond positively to treatment
- **Sure Things**: Will stay anyway, don't waste budget
- **Lost Causes**: Won't respond to treatment
- **Sleeping Dogs** (DO NOT CONTACT!): Treatment INCREASES churn

### RFM Segments

- **Champions**: Best customers, high R/F/M scores
- **Loyal Customers**: Regular buyers
- **At Risk**: Previously high-value, now declining
- **Can't Lose Them**: High value but haven't bought recently
- **Lost/Hibernating**: Long time since last activity
- **New Customers**: Recently acquired
- **Need Attention**: Below average across metrics

### Risk Levels

- **Critical (75-100)**: Immediate action required
- **High (50-74)**: Plan intervention soon
- **Medium (25-49)**: Monitor closely
- **Low (0-24)**: Maintain current engagement

## Common Use Cases

### Use Case 1: Win-Back Campaign

```python
# Get all high-risk customers who are Persuadables
response = requests.post(
    f"{API_BASE}/behavior/customers/churn-risk?dataset_id={dataset_id}",
    json={
        "min_risk_score": 70,
        "segment": "At Risk",
        "limit": 500
    },
    headers=headers
)

high_risk = response.json()["results"]

# Get interventions for them
interventions = requests.post(
    f"{API_BASE}/behavior/interventions/recommend?dataset_id={dataset_id}",
    json={
        "customer_ids": [c["customer_id"] for c in high_risk],
        "min_uplift_threshold": 0.2,  # Only target strong responders
        "budget": 50000,
        "industry": "ecommerce"
    },
    headers=headers
).json()

print(f"Recommended {len(interventions['interventions'])} interventions")
print(f"Expected total value: ${interventions['expected_total_value']:,.2f}")
print(f"ROI: {(interventions['expected_total_value'] / interventions['total_budget_allocated'] * 100):.0f}%")
```

### Use Case 2: Segment Analysis

```python
# Get stats
stats = requests.get(
    f"{API_BASE}/behavior/datasets/{dataset_id}/stats",
    headers=headers
).json()

# Analyze segments
for segment, count in stats["segments"].items():
    pct = (count / stats["total_customers"]) * 100
    print(f"{segment}: {count} ({pct:.1f}%)")
```

### Use Case 3: Customer Journey

```python
# Get behavior for a customer
customer_id = "12345"
behavior = requests.get(
    f"{API_BASE}/behavior/customers/{customer_id}/behavior?dataset_id={dataset_id}",
    headers=headers
).json()

print(f"Customer: {customer_id}")
print(f"Segment: {behavior['segment']}")
print(f"Churn Risk: {behavior['churn_risk_score']:.1f}%")
print(f"Engagement: {behavior['engagement']['engagement_score']}")
print(f"Trends: {', '.join(behavior['insights']['trends'])}")
print("\nRecommendations:")
for rec in behavior['recommendations']:
    print(f"  [{rec['priority']}] {rec['action']}")
```

## Next Steps

1. **Integrate with your CRM**: Use the intervention recommendations to trigger email campaigns
2. **A/B Test**: Validate the uplift model predictions with real campaigns
3. **Monitor ROI**: Track actual retention vs predicted
4. **Customize**: Adjust intervention configs for your industry
5. **Scale**: Process larger datasets (tested up to 1M customers)

## Troubleshooting

**Q: Upload fails with "File too large"**
A: Increase file size limit in nginx/gunicorn config (default: 100MB)

**Q: Processing stuck at "normalizing"**
A: Check logs in `backend/logs/`. Likely missing required columns.

**Q: All uplift scores are near zero**
A: Your treatment may not have significant effect. Check treatment/control balance.

**Q: Models not training**
A: Minimum requirements:
- 1,000+ total customers
- 100+ in treatment group
- 100+ in control group

## Documentation

- Full API documentation: http://localhost:5000/docs
- Detailed guide: [docs/BEHAVIOR_ANALYSIS.md](docs/BEHAVIOR_ANALYSIS.md)
- Dataset formats: See `BEHAVIOR_ANALYSIS.md` - Dataset Formats section

## Support

For issues: https://github.com/your-repo/issues
