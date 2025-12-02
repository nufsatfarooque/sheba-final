# Complete Setup and Execution Guide
## Customer Behavior Analysis with Real Datasets

This guide provides **explicit, step-by-step instructions** for setting up and running the customer behavior analysis feature with **actual real-world datasets**.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Database Setup](#database-setup)
4. [Download Real Datasets](#download-real-datasets)
5. [Start the System](#start-the-system)
6. [Upload and Process Datasets](#upload-and-process-datasets)
7. [Access and Use the System](#access-and-use-the-system)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python 3.8+** (Recommended: 3.10 or 3.11)
- **Node.js 16+** (Recommended: 18 or 20)
- **PostgreSQL 12+** (or SQLite for testing)
- **Git**

### Check Your Setup
```bash
# Check Python version
python --version  # Should be 3.8+

# Check Node.js version
node --version  # Should be 16+

# Check npm version
npm --version

# Check PostgreSQL (if using)
psql --version
```

---

## Initial Setup

### Step 1: Clone and Navigate to Project
```bash
cd d:/coding/projects/sheba-final
```

### Step 2: Install Backend Dependencies
```bash
cd backend

# Install main dependencies
pip install -r requirements.txt

# Install behavior analysis specific dependencies
pip install -r requirements_behavior_analysis.txt
```

**Expected packages for behavior analysis:**
- `scikit-learn>=1.3.0` - Machine learning models
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical computing
- `scipy>=1.10.0` - Scientific computing
- `matplotlib>=3.7.0` - Visualization
- `seaborn>=0.12.0` - Statistical visualization

### Step 3: Install Frontend Dependencies
```bash
cd ../frontend
npm install
```

### Step 4: Configure Environment Variables

Create `.env` file in `backend/` directory:
```bash
cd ../backend
```

**For PostgreSQL (Production):**
```env
DATABASE_URL=postgresql://username:password@localhost:5432/sheba_db
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**For SQLite (Testing):**
```env
DATABASE_URL=sqlite:///./sheba.db
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Database Setup

### Step 1: Run Migrations

The migration file for behavior analysis tables already exists. Run:

```bash
cd backend

# Run all migrations (including behavior analysis tables)
alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 9087b40beb09, initial migration
INFO  [alembic.runtime.migration] Running upgrade 9087b40beb09 -> a1b2c3d4e5f6, add role and is_active to users
INFO  [alembic.runtime.migration] Running upgrade a1b2c3d4e5f6 -> behavior_001, add behavior analysis tables
```

### Step 2: Verify Tables Created

**PostgreSQL:**
```bash
psql -U username -d sheba_db -c "\dt"
```

**SQLite:**
```bash
sqlite3 sheba.db ".tables"
```

**Expected tables:**
- `users` - User authentication
- `datasets` - Dataset metadata and processing status
- `customers` - Normalized customer records with RFM scores
- `customer_behavior_summaries` - Behavior analysis results
- `interventions` - Intervention recommendations

---

## Download Real Datasets

### Step 1: Run Dataset Download Script

```bash
cd backend
python scripts/download_real_datasets.py
```

This script will:
1. **Criteo Dataset** - Generate sample (full dataset is 25GB+, requires manual download)
2. **Hillstrom Dataset** - Download from public source or generate sample
3. **IBM Telco Dataset** - Download from IBM/GitHub or generate sample
4. **Financial Services** - Generate synthetic dataset based on real patterns
5. **B2B SaaS** - Generate synthetic dataset based on real patterns

**Output location:** `backend/data/real_datasets/`

**Expected files:**
- `criteo_uplift.csv` (~10,000 records)
- `hillstrom_email.csv` (~10,000 records)
- `telco_churn.csv` (~7,000 records)
- `financial_services.csv` (~10,000 records)
- `b2b_saas.csv` (~5,000 records)

### Step 2: (Optional) Download Full Criteo Dataset

For the **full Criteo dataset**:

1. Visit: https://ailab.criteo.com/criteo-uplift-prediction-dataset/
2. Download the training set (25GB+ compressed)
3. Extract and save to: `backend/data/real_datasets/criteo_uplift.csv`

**Warning:** The full dataset has 13.9M records and requires significant processing time.

---

## Start the System

### Step 1: Create a User Account

First, start the backend to create a user:

```bash
cd backend
python -m uvicorn app.main:app --reload --port 5000
```

Then, create a user via API:

```bash
curl -X POST "http://localhost:5000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "SecurePassword123",
    "full_name": "Admin User"
  }'
```

Or start the frontend and sign up through the UI.

### Step 2: Start Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload --port 5000
```

**Server will be available at:**
- API: http://localhost:5000
- API Docs: http://localhost:5000/docs
- OpenAPI Schema: http://localhost:5000/openapi.json

**Expected console output:**
```
INFO:     Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 3: Start Frontend Server (New Terminal)

```bash
cd frontend
npm run dev
```

**Frontend will be available at:**
- http://localhost:5173

**Expected console output:**
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

---

## Upload and Process Datasets

You have **three options** for uploading datasets:

### Option A: Automated Upload Script (Recommended)

```bash
cd backend

# Upload all datasets
python scripts/upload_datasets.py \
  --email admin@example.com \
  --password SecurePassword123 \
  --wait

# Or upload specific datasets
python scripts/upload_datasets.py \
  --email admin@example.com \
  --password SecurePassword123 \
  --datasets telco hillstrom
```

**The `--wait` flag** will monitor processing until completion.

**Expected output:**
```
2024-12-02 10:00:00 - INFO - ===================================
2024-12-02 10:00:00 - INFO - UPLOADING DATASETS TO BEHAVIOR ANALYSIS SYSTEM
2024-12-02 10:00:00 - INFO - ===================================
2024-12-02 10:00:00 - INFO - Logging in as admin@example.com...
2024-12-02 10:00:01 - INFO - ✓ Login successful
2024-12-02 10:00:01 - INFO - Uploading Criteo Uplift Dataset (criteo)...
2024-12-02 10:00:05 - INFO - ✓ Upload successful - Dataset ID: abc123...
2024-12-02 10:00:05 - INFO -   Status: processing
...
```

### Option B: Manual Upload via cURL

**Step 1: Login and Get Token**
```bash
TOKEN=$(curl -X POST "http://localhost:5000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=SecurePassword123" \
  | jq -r '.access_token')

echo $TOKEN
```

**Step 2: Upload Dataset**
```bash
curl -X POST "http://localhost:5000/api/v1/behavior/upload-data" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@data/real_datasets/telco_churn.csv" \
  -F "dataset_name=IBM Telco Customer Churn" \
  -F "dataset_type=telco" \
  -F "auto_train=true"
```

**Response:**
```json
{
  "dataset_id": "abc123-def456-...",
  "status": "processing",
  "message": "Dataset uploaded successfully. Processing in background."
}
```

**Step 3: Check Processing Status**
```bash
DATASET_ID="abc123-def456-..."

curl -X GET "http://localhost:5000/api/v1/behavior/data/status/$DATASET_ID" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "dataset_id": "abc123-def456-...",
  "name": "IBM Telco Customer Churn",
  "status": "completed",
  "total_records": 7043,
  "treatment_count": 1760,
  "control_count": 5283,
  "churn_rate_treatment": 0.18,
  "churn_rate_control": 0.27,
  "created_at": "2024-12-02T10:00:00Z",
  "completed_at": "2024-12-02T10:05:30Z"
}
```

### Option C: Upload via Web UI

1. Navigate to http://localhost:5173/
2. Login with your credentials
3. Go to http://localhost:5173/behavior-analysis
4. Use the upload form:
   - **Dataset Name**: e.g., "IBM Telco Customer Churn"
   - **Dataset Type**: Select from dropdown (Criteo, Hillstrom, Financial, B2B, Telco)
   - **CSV File**: Choose file from `data/real_datasets/`
   - Click **Upload & Process**

**The UI will show:**
- Upload progress bar
- Processing status
- Dataset statistics when complete

---

## Access and Use the System

### 1. View All Datasets

**API:**
```bash
curl -X GET "http://localhost:5000/api/v1/behavior/datasets" \
  -H "Authorization: Bearer $TOKEN"
```

**UI:**
- Navigate to http://localhost:5173/behavior-analysis
- View list of uploaded datasets

### 2. Get Dataset Statistics

**API:**
```bash
curl -X GET "http://localhost:5000/api/v1/behavior/datasets/$DATASET_ID/stats" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "dataset_id": "abc123...",
  "total_customers": 7043,
  "segments": {
    "Champions": 850,
    "Loyal Customers": 1200,
    "At Risk": 1800,
    "Can't Lose Them": 600,
    "Lost/Hibernating": 1100,
    "New Customers": 950,
    "Need Attention": 543
  },
  "risk_levels": {
    "Critical": 1100,
    "High": 2200,
    "Medium": 2500,
    "Low": 1243
  },
  "avg_churn_risk": 45.2,
  "avg_clv": 1250.00,
  "treatment_effect": 0.09
}
```

**UI:**
- Click on a dataset in the list
- View statistics dashboard with charts

### 3. Get High-Risk Customers

**API:**
```bash
curl -X POST "http://localhost:5000/api/v1/behavior/customers/churn-risk?dataset_id=$DATASET_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "min_risk_score": 70,
    "limit": 20
  }'
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
  "total_count": 1523,
  "status": "success"
}
```

### 4. Get Customer Behavior Analysis

**API:**
```bash
curl -X GET "http://localhost:5000/api/v1/behavior/customers/TELCO000042/behavior?dataset_id=$DATASET_ID" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "customer_id": "TELCO000042",
  "churn_risk_score": 78.5,
  "segment": "At Risk",
  "customer_type": "Persuadable",
  "profile": {
    "segment": "At Risk",
    "tenure": "365 days",
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
      "💰 Medium-value customer at risk"
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
      "action": "Offer retention incentive (15-20% discount)",
      "reason": "Prevent imminent churn of valuable customer",
      "expected_impact": "High",
      "timing": "Within 24 hours"
    }
  ],
  "generated_at": "2024-12-02T10:30:00Z"
}
```

### 5. Get Intervention Recommendations

**API:**
```bash
curl -X POST "http://localhost:5000/api/v1/behavior/interventions/recommend?dataset_id=$DATASET_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "min_uplift_threshold": 0.15,
    "budget": 10000,
    "max_interventions": 50,
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
      "message_body": "As a valued customer, we'd like to offer you 15% off your next 6 months",
      "recommended_timing": "immediate"
    }
  ],
  "total_recommended": 25,
  "total_budget_allocated": 7500.00,
  "expected_total_value": 42500.00,
  "status": "success"
}
```

---

## Processing Timeline

**Expected processing times** for each dataset:

| Dataset | Records | Upload | Processing | Total Time |
|---------|---------|--------|------------|------------|
| Criteo (sample) | 10,000 | ~5s | ~3min | ~3-4min |
| Hillstrom | 10,000 | ~5s | ~3min | ~3-4min |
| Telco | 7,043 | ~3s | ~2min | ~2-3min |
| Financial | 10,000 | ~5s | ~3min | ~3-4min |
| B2B SaaS | 5,000 | ~2s | ~1.5min | ~2min |

**Processing includes:**
1. CSV validation and parsing
2. Schema normalization to universal RFM framework
3. Feature engineering (RFM scores, behavioral metrics)
4. ML model training (churn prediction + uplift modeling)
5. Customer behavior summary generation
6. Intervention recommendation calculation

---

## Dataset Details

### 1. Criteo Uplift Dataset
- **Source**: Criteo AI Lab
- **Size**: 10,000 records (sample) or 13.9M (full)
- **Purpose**: Ad click uplift modeling
- **Features**: 12 anonymized features (f0-f11)
- **Outcome**: Conversion (purchase)
- **Use Case**: Digital advertising optimization

### 2. Hillstrom Email Marketing Dataset
- **Source**: Kevin Hillstrom MineThatData Challenge
- **Size**: 10,000 records
- **Purpose**: Email marketing campaign effectiveness
- **Features**: Recency, history, demographics, channel
- **Outcome**: Purchase, visit
- **Use Case**: Email campaign ROI optimization

### 3. IBM Telco Customer Churn Dataset
- **Source**: IBM Watson Analytics
- **Size**: 7,043 customers
- **Purpose**: Telecom customer retention
- **Features**: Services, contract, billing, demographics
- **Outcome**: Churn (Yes/No)
- **Use Case**: Retention campaign targeting

### 4. Financial Services Dataset (Synthetic)
- **Size**: 10,000 customers
- **Purpose**: Banking/FinTech churn prediction
- **Features**: Transactions, balance, products, satisfaction
- **Outcome**: Account closure
- **Use Case**: Customer relationship management

### 5. B2B SaaS Dataset (Synthetic)
- **Size**: 5,000 companies
- **Purpose**: B2B subscription retention
- **Features**: Usage, seats, support, contract value
- **Outcome**: Subscription cancellation
- **Use Case**: Customer success interventions

---

## Troubleshooting

### Issue: Migration Fails

**Error:** `Table 'datasets' already exists`

**Solution:**
```bash
cd backend
alembic downgrade -1  # Downgrade one version
alembic upgrade head   # Re-run migration
```

### Issue: Upload Fails - File Too Large

**Error:** `413 Request Entity Too Large`

**Solution:**
Increase file size limit in `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add this
from fastapi.middleware.httpsexception import HTTPException
app.add_middleware(
    HTTPException,
    max_upload_size=500_000_000  # 500MB
)
```

### Issue: Processing Stuck

**Error:** Dataset status stays at "processing" for >10 minutes

**Solution:**
1. Check backend logs for errors
2. Verify minimum data requirements:
   - At least 1,000 customers
   - At least 100 in treatment group
   - At least 100 in control group
3. Check dataset format matches expected schema

### Issue: Low/Zero Uplift Scores

**Cause:** Treatment may not have real effect in data

**Solution:**
1. Check treatment/control group balance
2. Verify treatment column has variation
3. Check outcome distribution
4. Try different datasets

### Issue: Frontend Can't Connect to Backend

**Error:** `Network Error` or `CORS Error`

**Solution:**
1. Verify backend is running on port 5000
2. Check CORS settings in `backend/app/main.py`
3. Ensure API_BASE in frontend matches backend URL

### Issue: Database Connection Error

**Error:** `Could not connect to database`

**Solution:**
For PostgreSQL:
```bash
# Check if PostgreSQL is running
pg_isready

# Restart PostgreSQL
sudo service postgresql restart
```

For SQLite:
```bash
# Verify database file exists
ls -la backend/sheba.db

# If missing, run migrations again
cd backend
alembic upgrade head
```

---

## Understanding the Output

### Customer Types (From Uplift Modeling)

1. **Persuadables** (Target These!) - Will respond positively to treatment
   - Uplift score > 0.1
   - High ROI
   - Priority for intervention

2. **Sure Things** - Will stay anyway
   - Low uplift, low churn risk
   - Don't waste budget

3. **Lost Causes** - Won't respond to treatment
   - Low uplift, high churn risk
   - Consider long-term strategies

4. **Sleeping Dogs** (DO NOT CONTACT!) - Treatment INCREASES churn
   - Negative uplift score
   - Avoid intervention

### RFM Segments

- **Champions** - Best customers (R=5, F=5, M=5)
- **Loyal Customers** - Regular buyers
- **At Risk** - Previously high-value, declining
- **Can't Lose Them** - High value but inactive
- **Lost/Hibernating** - Long inactive period
- **New Customers** - Recently acquired
- **Need Attention** - Below average metrics

### Risk Levels

- **Critical (75-100)** - Immediate action required
- **High (50-74)** - Plan intervention within 24-48 hours
- **Medium (25-49)** - Monitor closely
- **Low (0-24)** - Maintain current engagement

---

## Next Steps

1. **Integrate with CRM/Marketing Automation**
   - Export intervention recommendations
   - Trigger campaigns via API

2. **A/B Test the Predictions**
   - Validate uplift model with real campaigns
   - Track actual vs. predicted retention

3. **Monitor ROI**
   - Track intervention costs
   - Measure actual customer retention
   - Calculate true ROI

4. **Customize for Your Industry**
   - Adjust intervention types
   - Modify cost assumptions
   - Tune thresholds

5. **Scale to Production**
   - Process larger datasets
   - Optimize performance
   - Add automated retraining

---

## API Reference

Full API documentation available at: http://localhost:5000/docs

**Key Endpoints:**
- `POST /api/v1/behavior/upload-data` - Upload dataset
- `GET /api/v1/behavior/datasets` - List all datasets
- `GET /api/v1/behavior/data/status/{dataset_id}` - Check processing status
- `GET /api/v1/behavior/datasets/{dataset_id}/stats` - Get statistics
- `POST /api/v1/behavior/customers/churn-risk` - Get high-risk customers
- `GET /api/v1/behavior/customers/{customer_id}/behavior` - Get behavior analysis
- `POST /api/v1/behavior/interventions/recommend` - Get interventions

---

## Support

- **Documentation**: See `docs/BEHAVIOR_ANALYSIS.md`
- **API Docs**: http://localhost:5000/docs
- **Sample Data**: `backend/data/sample_datasets/`
- **Real Data**: `backend/data/real_datasets/`

For issues, check the troubleshooting section or review backend logs.
