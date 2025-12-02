# Quick Start: Running Customer Behavior Analysis with Real Data

**Goal:** Get the behavior analysis system running with real datasets in **under 15 minutes**.

---

## Prerequisites Check (2 minutes)

```bash
# Verify installations
python --version   # Should be 3.8+
node --version     # Should be 16+
psql --version     # Or use SQLite

# Navigate to project
cd d:/coding/projects/sheba-final
```

---

## Step 1: Install Dependencies (3 minutes)

### Backend
```bash
cd backend
pip install -r requirements.txt
pip install -r requirements_behavior_analysis.txt
```

### Frontend
```bash
cd ../frontend
npm install
```

---

## Step 2: Setup Database (1 minute)

### Option A: SQLite (Quick Test)
```bash
cd ../backend

# Create .env file
echo "DATABASE_URL=sqlite:///./sheba.db" > .env
echo "SECRET_KEY=your-secret-key-change-in-production" >> .env

# Run migrations
alembic upgrade head
```

### Option B: PostgreSQL (Production)
```bash
cd ../backend

# Create .env file
echo "DATABASE_URL=postgresql://user:pass@localhost:5432/sheba_db" > .env
echo "SECRET_KEY=your-secret-key-change-in-production" >> .env

# Run migrations
alembic upgrade head
```

**Expected Output:**
```
INFO  [alembic.runtime.migration] Running upgrade a1b2c3d4e5f6 -> behavior_001, add behavior analysis tables
```

---

## Step 3: Download Real Datasets (2 minutes)

```bash
cd backend
python scripts/download_real_datasets.py
```

**This creates 5 datasets in `data/real_datasets/`:**
- ✅ `criteo_uplift.csv` (10,000 records)
- ✅ `hillstrom_email.csv` (10,000 records)
- ✅ `telco_churn.csv` (7,043 records)
- ✅ `financial_services.csv` (10,000 records)
- ✅ `b2b_saas.csv` (5,000 records)

---

## Step 4: Start the System (1 minute)

### Terminal 1: Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --port 5000
```

**Expected:** `Uvicorn running on http://127.0.0.1:5000`

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

**Expected:** `Local: http://localhost:5173/`

---

## Step 5: Create User Account (1 minute)

### Option A: Via API
```bash
curl -X POST "http://localhost:5000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "Admin123!",
    "full_name": "Admin User"
  }'
```

### Option B: Via UI
1. Go to http://localhost:5173/signup
2. Fill in details and create account
3. Login at http://localhost:5173/login

---

## Step 6: Upload Datasets (5 minutes)

### Option A: Web UI (Recommended)

1. **Navigate to:** http://localhost:5173/behavior-analysis

2. **Upload each dataset:**

   **Dataset 1: IBM Telco**
   - Dataset Name: `IBM Telco Customer Churn`
   - Dataset Type: `Telco`
   - File: Browse to `backend/data/real_datasets/telco_churn.csv`
   - Click **Upload & Process**

   **Dataset 2: Hillstrom Email**
   - Dataset Name: `Hillstrom Email Marketing Campaign`
   - Dataset Type: `Hillstrom`
   - File: `backend/data/real_datasets/hillstrom_email.csv`
   - Click **Upload & Process**

   **Dataset 3: Financial Services**
   - Dataset Name: `Financial Services Customer Data`
   - Dataset Type: `Financial`
   - File: `backend/data/real_datasets/financial_services.csv`
   - Click **Upload & Process**

3. **Wait for processing:** Each dataset takes 2-4 minutes

### Option B: API Upload

**Login:**
```bash
TOKEN=$(curl -X POST "http://localhost:5000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=Admin123!" \
  | jq -r '.access_token')
```

**Upload Telco Dataset:**
```bash
curl -X POST "http://localhost:5000/api/v1/behavior/upload-data" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@data/real_datasets/telco_churn.csv" \
  -F "dataset_name=IBM Telco Customer Churn" \
  -F "dataset_type=telco" \
  -F "auto_train=true"
```

**Save the dataset_id from response:**
```json
{
  "dataset_id": "abc123-def456-...",
  "status": "processing",
  "message": "Dataset uploaded successfully"
}
```

---

## Step 7: Explore Results (3 minutes)

### Via Web UI

**After processing completes:**

1. **View Dataset Statistics**
   - Click on a completed dataset in the list
   - See customer segments, risk levels, treatment effect

2. **Expected Output:**
   ```
   Total Customers: 7,043
   Avg Churn Risk: 45.2%
   Avg CLV: $1,250
   Treatment Effect: 9% churn reduction

   Segments:
   - Champions: 850 (12%)
   - At Risk: 1,800 (26%)
   - Lost: 1,100 (16%)
   ...
   ```

### Via API

**Get Dataset Statistics:**
```bash
DATASET_ID="<your-dataset-id>"

curl -X GET "http://localhost:5000/api/v1/behavior/datasets/$DATASET_ID/stats" \
  -H "Authorization: Bearer $TOKEN"
```

**Get High-Risk Customers:**
```bash
curl -X POST "http://localhost:5000/api/v1/behavior/customers/churn-risk?dataset_id=$DATASET_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"min_risk_score": 70, "limit": 10}'
```

**Response:**
```json
{
  "results": [
    {
      "customer_id": "TELCO000042",
      "churn_risk_score": 78.5,
      "risk_level": "High",
      "segment": "At Risk",
      "uplift_score": 0.42,
      "clv_estimate": 2500.00
    }
  ],
  "total_count": 1523
}
```

**Get Customer Behavior Analysis:**
```bash
curl -X GET "http://localhost:5000/api/v1/behavior/customers/TELCO000042/behavior?dataset_id=$DATASET_ID" \
  -H "Authorization: Bearer $TOKEN"
```

**Response includes:**
- Profile (segment, tenure, lifecycle stage)
- Engagement metrics (activity level, trend, score)
- Value analysis (spending patterns, CLV)
- Risk indicators
- Personalized recommendations

**Get Intervention Recommendations:**
```bash
curl -X POST "http://localhost:5000/api/v1/behavior/interventions/recommend?dataset_id=$DATASET_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "min_uplift_threshold": 0.15,
    "budget": 10000,
    "industry": "telco"
  }'
```

**Response:**
```json
{
  "interventions": [
    {
      "customer_id": "TELCO000042",
      "treatment_id": "retention_offer_15pct",
      "intervention_type": "discount",
      "channel": "in_app",
      "uplift_score": 0.68,
      "expected_value": 1700.00,
      "roi": 467.0,
      "cost": 300.00,
      "message_body": "As a valued customer, get 15% off your next 6 months",
      "recommended_timing": "immediate"
    }
  ],
  "total_recommended": 25,
  "total_budget_allocated": 7500.00,
  "expected_total_value": 42500.00
}
```

---

## What Just Happened?

### Automatic Schema Normalization

Your datasets were automatically normalized to a universal schema:

**Telco Dataset:**
```
Original:
  customerID, tenure (months), MonthlyCharges, Churn (Yes/No)

Normalized to:
  customer_id, tenure_days (×30), total_value_30d, outcome (0/1)
```

**Hillstrom Dataset:**
```
Original:
  recency (months), history (total spend), mens/womens (email type)

Normalized to:
  days_since_last_activity (×30), total_value_90d, treatment_type
```

See [DATASET_FORMATS_AND_NORMALIZATION.md](DATASET_FORMATS_AND_NORMALIZATION.md) for details.

### ML Models Trained

For each dataset:
1. **Churn Prediction Model** - RF + Gradient Boosting ensemble
2. **Uplift Model** - X-Learner for treatment effect
3. **Customer Segmentation** - RFM-based clustering

### Behavior Analysis Generated

For every customer:
- Churn risk score (0-100)
- Customer segment (Champions, At Risk, etc.)
- Uplift score (treatment effect)
- Personalized interventions
- Expected ROI

---

## Key URLs

| Resource | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Behavior Analysis UI | http://localhost:5173/behavior-analysis |
| Backend API | http://localhost:5000 |
| API Documentation | http://localhost:5000/docs |

---

## Dataset Processing Status

Monitor processing in:
- **UI:** Datasets list shows status badge
- **API:** `GET /api/v1/behavior/data/status/{dataset_id}`

**Status Values:**
- `uploading` - File being saved
- `processing` - Parsing CSV
- `normalizing` - Schema transformation
- `completed` - Ready to use ✓
- `failed` - Error occurred ✗

---

## Sample Insights You'll See

### Telco Dataset (7,043 customers)
- **Churn Rate:** 26.5%
- **Treatment Effect:** 9% churn reduction
- **High-Risk Customers:** 1,523 (22%)
- **Persuadables (Target):** 892 customers
- **Expected ROI:** 350-500% for targeted interventions

### Hillstrom Dataset (10,000 customers)
- **Email Campaign Effectiveness:**
  - Control: 10% conversion
  - Mens Email: 18% conversion (+80%)
  - Womens Email: 15% conversion (+50%)
- **Best Uplift Segment:** Recent buyers (recency < 3 months)

### Financial Dataset (10,000 customers)
- **Avg Churn Risk:** 42%
- **High-Value At-Risk:** 450 customers
- **Intervention Budget:** $10K → Expected value: $45K

---

## Common Use Cases

### 1. Win-Back Campaign
**Find high-risk customers who will respond to offers:**

```bash
curl -X POST ".../behavior/customers/churn-risk?dataset_id=$ID" \
  -d '{"min_risk_score": 70, "limit": 100}'

# Then get interventions for them
curl -X POST ".../behavior/interventions/recommend?dataset_id=$ID" \
  -d '{"customer_ids": [...], "min_uplift_threshold": 0.2, "budget": 50000}'
```

### 2. Customer Health Dashboard
**Monitor segments over time:**

```bash
curl -X GET ".../behavior/datasets/$ID/stats"
```

Track:
- % in each RFM segment
- Average churn risk by segment
- Treatment effect validation

### 3. Personalized Engagement
**Get recommendations for individual customers:**

```bash
curl -X GET ".../behavior/customers/$CUSTOMER_ID/behavior?dataset_id=$ID"
```

Returns:
- Current risk level
- Recommended actions
- Best channel & timing
- Expected impact

---

## Troubleshooting

### Processing Stuck?
Check backend logs for errors. Common issues:
- Missing required columns → See dataset format guide
- Invalid data types → Ensure numbers are numeric
- Insufficient data → Need 1000+ customers, 100+ treatment/control

### No Uplift Detected?
- Verify treatment column has both 0 and 1 values
- Check if treatment actually had an effect in data
- Ensure control/treatment groups are balanced

### Frontend Can't Connect?
- Verify backend is running on port 5000
- Check CORS settings in backend
- Ensure API_BASE in frontend matches backend URL

---

## Next Steps

1. **Upload More Datasets** - Try all 5 dataset types

2. **Export Interventions** - Integrate with your CRM/marketing automation

3. **A/B Test Predictions** - Validate uplift model with real campaigns

4. **Monitor ROI** - Track actual vs predicted retention

5. **Customize for Your Industry** - Adjust intervention types and costs

6. **Scale to Production** - Process larger datasets, automate retraining

---

## Full Documentation

- **Complete Setup Guide:** [SETUP_AND_RUN_GUIDE.md](SETUP_AND_RUN_GUIDE.md)
- **Dataset Formats:** [DATASET_FORMATS_AND_NORMALIZATION.md](DATASET_FORMATS_AND_NORMALIZATION.md)
- **Feature Documentation:** [docs/BEHAVIOR_ANALYSIS.md](docs/BEHAVIOR_ANALYSIS.md)
- **API Reference:** http://localhost:5000/docs

---

## Support

For issues or questions:
1. Check [SETUP_AND_RUN_GUIDE.md](SETUP_AND_RUN_GUIDE.md) troubleshooting section
2. Review backend logs
3. Verify dataset format matches expected schema
4. Check database migration status

**You're all set!** The system is running with real data and generating actionable customer insights.
