# Dataset Formats and Schema Normalization Guide

This guide explains **how your datasets are automatically normalized** to our universal RFM (Recency, Frequency, Monetary) schema.

---

## Overview

The system accepts **5 different dataset formats** and automatically normalizes them to a universal schema. This allows the same ML models and behavior analysis to work across all industries.

**Supported Formats:**
1. **Criteo** - Advertising/Marketing (anonymized features)
2. **Hillstrom** - Email Marketing campaigns
3. **Financial Services** - Banking/FinTech customer data
4. **B2B SaaS** - Enterprise software subscriptions
5. **Telco** - Telecommunications customer churn

---

## Universal RFM Schema

All datasets are normalized to this structure:

```python
{
    # === IDENTITY ===
    "customer_id": str,              # Unique customer identifier

    # === TREATMENT & OUTCOME ===
    "treatment": int,                # 0 = control, 1 = treatment
    "treatment_type": str,           # e.g., "email_campaign", "discount", "call"
    "outcome": int,                  # 0 = retained, 1 = churned

    # === RECENCY (How recently active?) ===
    "days_since_last_activity": float,  # Days since last action
    "recency_score": int,            # 1-5 (5 = most recent)

    # === FREQUENCY (How often active?) ===
    "activity_count_30d": int,       # Activities in last 30 days
    "activity_count_90d": int,       # Activities in last 90 days
    "frequency_score": int,          # 1-5 (5 = most frequent)

    # === MONETARY (How valuable?) ===
    "total_value_30d": float,        # Revenue/value in last 30 days (USD)
    "total_value_90d": float,        # Revenue/value in last 90 days (USD)
    "avg_value_per_activity": float, # Average transaction value (USD)
    "monetary_score": int,           # 1-5 (5 = highest value)

    # === COMBINED ===
    "rfm_score": int,                # 3-15 (sum of R+F+M scores)

    # === BEHAVIORAL ===
    "tenure_days": int,              # How long a customer
    "engagement_score": float,       # 0-100 engagement index
    "activity_trend": float,         # % change in activity (-1 to +1)
    "feature_usage_count": int,      # Number of features/products used
    "session_count_30d": int,        # Sessions in last 30 days

    # === SUPPORT/SERVICE ===
    "support_tickets_30d": int,      # Support requests
    "satisfaction_score": float,     # 0-100 CSAT/NPS proxy

    # === FINANCIAL ===
    "payment_failures": int,         # Failed payment attempts
    "account_balance": float,        # Current account value/balance (USD)

    # === PREDICTIONS (computed after upload) ===
    "churn_risk_score": float,       # 0-100 churn probability
    "uplift_score": float,           # Treatment effect prediction
    "customer_segment": str,         # "Champions", "At Risk", etc.
    "clv_estimate": float,           # Customer Lifetime Value (USD)
}
```

---

## Dataset-Specific Mappings

### 1. Criteo Uplift Dataset

**Source:** Criteo AI Lab Uplift Modeling Dataset
**Size:** 13.9M records (full), 10K (sample)
**Industry:** Digital Advertising

#### Required Columns:
```csv
f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, treatment, exposure, visit, conversion
```

#### Column Mapping:
| Criteo Column | Universal Schema | Description |
|---------------|------------------|-------------|
| `treatment` | `treatment` | 1 = shown ad, 0 = control |
| `conversion` | `outcome` | **Inverted:** 1-conversion (0=retained, 1=churned) |
| `f0` | `days_since_last_activity` | Recency proxy |
| `f1` | `tenure_days` | Account age |
| `f2` | `engagement_score` | Engagement level (0-100) |
| `f3` | `activity_trend` | Activity change (-1 to +1) |
| `f4` | `activity_count_30d` | 30-day activity count |
| `f5` | `activity_count_90d` | 90-day activity count |
| `f6` | `feature_usage_count` | Features used |
| `f7` | `session_count_30d` | Monthly sessions |
| `f8` | `total_value_30d` | 30-day spending (USD) |
| `f9` | `total_value_90d` | 90-day spending (USD) |
| `f10` | `avg_value_per_activity` | Avg transaction (USD) |
| `f11` | `account_balance` | Account balance (USD) |

**Default Values:**
- `support_tickets_30d` = 0 (not available)
- `satisfaction_score` = 75.0 (neutral)
- `payment_failures` = 0

**Example:**
```csv
f0,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,treatment,exposure,visit,conversion
15.5,365,78.2,0.15,12,38,5,24,450.5,1200.3,37.5,5000,1,1,1,1
45.2,180,45.8,-0.22,3,15,2,8,120.0,380.0,25.3,2500,0,0,0,0
```

---

### 2. Hillstrom Email Marketing Dataset

**Source:** Kevin Hillstrom MineThatData Challenge
**Size:** 64,000 records
**Industry:** E-commerce Email Marketing

#### Required Columns:
```csv
recency, history, mens, womens, zip_code, newbie, channel, visit, conversion, spend
```

#### Column Mapping:
| Hillstrom Column | Universal Schema | Transformation |
|------------------|------------------|----------------|
| `mens` OR `womens` | `treatment` | 1 if either is 1, else 0 |
| `mens`/`womens` | `treatment_type` | "mens_email", "womens_email", or "control" |
| `conversion` | `outcome` | **Inverted:** 1-conversion |
| `recency` | `days_since_last_activity` | **Convert months → days** (×30) |
| `history` | Derives frequency & monetary | Used to calculate multiple fields |
| `history / 12` | `total_value_30d` | Assume even distribution |
| `history / 4` | `total_value_90d` | Last 3 months |
| `newbie` | `tenure_days` | 1 → 30 days, 0 → 365 days |
| `channel` | `feature_usage_count` | Multichannel=3, Web=2, Phone=1 |

**Derived Calculations:**
```python
# Frequency estimation
avg_order_value = history.median() / 4  # Assume 4 purchases/year
activity_count_90d = history / avg_order_value / 4
activity_count_30d = activity_count_90d / 3

# Engagement score
engagement_score = 80 if recency < 3 months else (60 if < 6 else 40)

# Activity trend
activity_trend = -0.3 if recency > 6 else (0.2 if recency < 3 else 0.0)
```

**Example:**
```csv
recency,history,mens,womens,zip_code,newbie,channel,visit,conversion,spend
2,500.50,1,0,Suburban,0,Web,1,1,75.00
8,250.00,0,0,Urban,1,Phone,0,0,0.00
```

**Normalized Output:**
```python
{
    "customer_id": "0",
    "treatment": 1,  # mens=1
    "treatment_type": "mens_email",
    "outcome": 0,  # converted (retained)
    "days_since_last_activity": 60,  # 2 months × 30
    "activity_count_90d": 4,
    "total_value_90d": 125.13,
    "engagement_score": 80.0,
    ...
}
```

---

### 3. Financial Services Dataset

**Source:** Custom/Synthetic
**Size:** 10,000 customers
**Industry:** Banking, FinTech

#### Required Columns:
```csv
customer_id, treatment, churned, age, gender, account_balance, transaction_count_30d,
transaction_count_90d, avg_transaction_value, products_owned, tenure_months,
last_login_days, support_tickets_90d, credit_score, satisfaction_score
```

#### Column Mapping:
| Financial Column | Universal Schema | Notes |
|------------------|------------------|-------|
| `customer_id` | `customer_id` | Direct mapping |
| `treatment` | `treatment` | Direct mapping |
| `churned` | `outcome` | Direct mapping |
| `last_login_days` | `days_since_last_activity` | Direct |
| `transaction_count_30d` | `activity_count_30d` | Direct |
| `transaction_count_90d` | `activity_count_90d` | Direct |
| `avg_transaction_value` | `avg_value_per_activity` | Direct |
| `account_balance` | `account_balance` | Direct |
| `tenure_months` | `tenure_days` | **Convert months → days** (×30) |
| `products_owned` | `feature_usage_count` | Direct |
| `support_tickets_90d` | `support_tickets_30d` | **Scale:** ×(30/90) |

**Derived Calculations:**
```python
# Monetary values
total_value_30d = transaction_count_30d × avg_transaction_value
total_value_90d = transaction_count_90d × avg_transaction_value

# Engagement score (0-100)
engagement = (
    50 - (days_since_last_activity × 0.5) +  # Recency penalty
    (transaction_count_30d × 2) +             # Activity bonus
    (products_owned × 3)                       # Product usage bonus
).clip(0, 100)

# Activity trend
activity_trend = (transaction_count_30d - transaction_count_30d_prev) / max(transaction_count_30d_prev, 1)
```

**Example:**
```csv
customer_id,treatment,churned,age,gender,account_balance,transaction_count_30d,transaction_count_90d,avg_transaction_value,products_owned,tenure_months,last_login_days,support_tickets_90d,satisfaction_score
CUST000042,1,0,45,M,15000.50,12,38,125.50,3,24,5,2,85.5
CUST000123,0,1,32,F,500.00,1,4,50.00,1,6,45,5,35.0
```

---

### 4. B2B SaaS Dataset

**Source:** Custom/Synthetic
**Size:** 5,000 companies
**Industry:** Enterprise Software

#### Required Columns:
```csv
customer_id, treatment, churned, contract_value_per_month, contract_duration_months,
feature_usage_count, days_since_last_login, api_calls_30d, seats_purchased,
seats_active, support_tickets, csat_score, industry, company_size, onboarding_completed
```

#### Column Mapping:
| B2B Column | Universal Schema | Transformation |
|------------|------------------|----------------|
| `customer_id` | `customer_id` | Direct |
| `treatment` | `treatment` | Direct |
| `churned` | `outcome` | Direct |
| `days_since_last_login` | `days_since_last_activity` | Direct |
| `api_calls_30d` | `activity_count_30d` | Proxy for API usage |
| `api_calls_30d × 3` | `activity_count_90d` | Estimated |
| `contract_value_per_month` | `total_value_30d` | Monthly MRR |
| `contract_value_per_month × 3` | `total_value_90d` | Quarterly ARR |
| `contract_value_per_month × 12` | `clv_estimate` | Annual value estimate |
| `contract_duration_months` | `tenure_days` | **Convert to days** (×30) |
| `feature_usage_count` | `feature_usage_count` | Direct |
| `seats_active` | `session_count_30d` | Proxy |
| `support_tickets` | `support_tickets_30d` | Direct |
| `csat_score` | `satisfaction_score` | Direct |
| `seats_active / seats_purchased` | Part of `engagement_score` | Utilization rate |

**Derived Calculations:**
```python
# Engagement score
seat_utilization = seats_active / seats_purchased
engagement_score = (
    50 +
    (seat_utilization × 30) +          # Up to +30 for full utilization
    (feature_usage_count × 0.5) +      # Feature adoption
    (onboarding_completed × 10) +       # Onboarding completion
    (-days_since_last_login × 0.3)     # Recency penalty
).clip(0, 100)

# Account balance (contract value)
account_balance = contract_value_per_month × contract_duration_months
```

**Example:**
```csv
customer_id,treatment,churned,contract_value_per_month,contract_duration_months,feature_usage_count,days_since_last_login,seats_purchased,seats_active,support_tickets,csat_score,onboarding_completed
B2B00042,1,0,999.00,12,25,2,25,23,1,88.5,1
B2B00123,0,1,199.00,3,5,30,10,3,6,45.0,0
```

---

### 5. Telco Customer Churn Dataset

**Source:** IBM Watson Analytics
**Size:** 7,043 customers
**Industry:** Telecommunications

#### Required Columns:
```csv
customerID, gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService,
MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection,
TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling,
PaymentMethod, MonthlyCharges, TotalCharges, Churn
```

**Optional for Uplift Analysis:**
```csv
treatment  # Add this column with 0/1 for retention campaign target
```

#### Column Mapping:
| Telco Column | Universal Schema | Transformation |
|--------------|------------------|----------------|
| `customerID` | `customer_id` | Direct |
| `treatment` | `treatment` | If present; otherwise random 25% |
| `Churn` | `outcome` | "Yes" → 1, "No" → 0 |
| `tenure` | `tenure_days` | **Convert months → days** (×30) |
| Derived | `days_since_last_activity` | Assume recent if active |
| Service count | `feature_usage_count` | Count of "Yes" services |
| `MonthlyCharges` | `total_value_30d` | Direct |
| `TotalCharges` | `total_value_90d` | Proxy (use quarterly) |
| `TotalCharges / tenure` | `avg_value_per_activity` | Average monthly |
| `TotalCharges` | `account_balance` | Lifetime value |
| Derived from services | `engagement_score` | Service adoption rate |
| Derived from contract | `support_tickets_30d` | Higher for short contracts |

**Service Counting:**
```python
services = [
    'PhoneService', 'MultipleLines', 'InternetService',
    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
    'TechSupport', 'StreamingTV', 'StreamingMovies'
]
feature_usage_count = sum(1 for svc in services if row[svc] == 'Yes')
```

**Engagement Score Calculation:**
```python
engagement_score = (
    40 +  # Base score
    (service_count × 5) +              # Up to +45 for 9 services
    (10 if Contract == 'Two year' else 5 if Contract == 'One year' else 0) +
    (5 if PaperlessBilling == 'Yes' else 0)
).clip(0, 100)
```

**Example:**
```csv
customerID,gender,SeniorCitizen,tenure,PhoneService,InternetService,Contract,MonthlyCharges,TotalCharges,Churn,treatment
7590-VHVEG,Female,0,1,No,DSL,Month-to-month,29.85,29.85,No,0
5575-GNVDE,Male,0,34,Yes,DSL,One year,56.95,1889.50,No,1
3668-QPYBK,Male,0,2,Yes,DSL,Month-to-month,53.85,108.15,Yes,0
```

**Normalized Output:**
```python
{
    "customer_id": "7590-VHVEG",
    "treatment": 0,
    "outcome": 0,  # No churn
    "tenure_days": 30,  # 1 month
    "days_since_last_activity": 2.0,  # Assumed recent
    "feature_usage_count": 2,  # Phone=No, Internet=Yes
    "total_value_30d": 29.85,
    "total_value_90d": 89.55,  # 3 months
    "account_balance": 29.85,
    "engagement_score": 55.0,
    ...
}
```

---

## Unit Normalization

The system **automatically detects and converts units**:

### Time Units
Detects based on column names and value ranges:

| Source Unit | Detection | Conversion to Days |
|-------------|-----------|-------------------|
| Seconds | `*second*` in name, max < 86400 | value / 86400 |
| Minutes | `*minute*`, `*min*` in name | value / 1440 |
| Hours | `*hour*`, `*hr*` in name | value / 24 |
| Days | `*day*` in name | value × 1 |
| Weeks | `*week*` in name | value × 7 |
| Months | `*month*` in name | value × 30 |
| Years | `*year*` in name | value × 365 |

### Monetary Units
Converts all currencies to USD:

| Currency | Rate (Simplified) |
|----------|-------------------|
| USD | 1.0 |
| EUR | 1.1 |
| GBP | 1.3 |
| BDT (Taka) | 0.0091 |
| INR (Rupee) | 0.012 |
| JPY (Yen) | 0.0067 |

**Note:** Use a real-time forex API in production!

---

## RFM Score Calculation

After normalization, RFM scores (1-5) are calculated:

### Recency Score
```python
if days_since_last_activity <= 7:
    recency_score = 5
elif days_since_last_activity <= 30:
    recency_score = 4
elif days_since_last_activity <= 90:
    recency_score = 3
elif days_since_last_activity <= 180:
    recency_score = 2
else:
    recency_score = 1
```

### Frequency Score
Based on 90-day activity quintiles:
```python
quantiles = activity_count_90d.quantile([0.2, 0.4, 0.6, 0.8])
frequency_score = 1 to 5 based on quintile
```

### Monetary Score
Based on 90-day value quintiles:
```python
quantiles = total_value_90d.quantile([0.2, 0.4, 0.6, 0.8])
monetary_score = 1 to 5 based on quintile
```

### Combined RFM Score
```python
rfm_score = recency_score + frequency_score + monetary_score  # 3 to 15
```

---

## Customer Segmentation

Based on RFM scores:

| Segment | Criteria | Description |
|---------|----------|-------------|
| **Champions** | R=5, F=5, M=5 | Best customers |
| **Loyal Customers** | R≥4, F≥4 | Regular buyers |
| **At Risk** | R≤2, F≥4 | Were active, now declining |
| **Can't Lose Them** | R≤2, M=5 | High value, inactive |
| **Lost/Hibernating** | R=1, F=1 | Long time gone |
| **New Customers** | R=5, F≤2 | Recent but few purchases |
| **Need Attention** | R=3, F=3 | Below average |

---

## Preparing Your Own Dataset

### Option 1: Match an Existing Format

Use one of the 5 formats above exactly as specified. The system will auto-detect and normalize.

### Option 2: Custom Format

Provide these **minimum required columns**:

**Required:**
- `customer_id` (string)
- `treatment` (0 or 1)
- `outcome` (0=retained, 1=churned)

**Highly Recommended (RFM):**
- `days_since_last_activity` (float, in days)
- `activity_count_30d` (int)
- `total_value_30d` (float, USD)

**Optional but Useful:**
- `tenure_days`, `feature_usage_count`, `satisfaction_score`
- `support_tickets_30d`, `payment_failures`
- Any other behavioral or demographic features

The system will:
1. Use provided columns directly
2. Fill missing fields with intelligent defaults
3. Calculate RFM scores
4. Generate predictions

---

## Upload Process

When you upload a dataset:

1. **Validation** - Check file format (must be CSV)
2. **Type Detection** - Select dataset type (criteo, hillstrom, financial, b2b, telco)
3. **Schema Normalization** - Map columns to universal schema
4. **Unit Conversion** - Convert time/currency units
5. **RFM Calculation** - Calculate recency, frequency, monetary scores
6. **Feature Engineering** - Derive additional behavioral features
7. **Model Training** - Train churn prediction + uplift models
8. **Behavior Analysis** - Generate customer summaries
9. **Interventions** - Calculate personalized recommendations

**Processing Time:**
- 5,000 records: ~2 minutes
- 10,000 records: ~3-4 minutes
- 50,000 records: ~15 minutes
- 100,000 records: ~30 minutes

---

## Example: Complete Flow

### Input (Hillstrom CSV):
```csv
recency,history,mens,womens,zip_code,newbie,channel,visit,conversion,spend
2,500.50,1,0,Suburban,0,Web,1,1,75.00
```

### Normalization Process:
```python
{
    # Direct mapping
    "treatment": 1,  # mens=1
    "treatment_type": "mens_email",
    "outcome": 0,  # 1 - conversion

    # Unit conversion
    "days_since_last_activity": 60,  # 2 months × 30
    "tenure_days": 365,  # newbie=0 → returning customer

    # Derivation
    "activity_count_90d": 4,  # history / avg_order_value
    "activity_count_30d": 1,  # activity_90d / 3
    "total_value_90d": 125.13,  # history / 4
    "total_value_30d": 41.71,  # history / 12

    # Calculation
    "engagement_score": 80.0,  # High (recency < 3)
    "feature_usage_count": 2,  # Web channel

    # Defaults
    "support_tickets_30d": 0,
    "payment_failures": 0,
}
```

### After RFM Calculation:
```python
{
    "recency_score": 4,  # 60 days → good
    "frequency_score": 3,  # 4 activities → moderate
    "monetary_score": 4,  # $125 → good
    "rfm_score": 11,  # 4+3+4
    "customer_segment": "Loyal Customers"
}
```

### After ML Models:
```python
{
    "churn_risk_score": 18.5,  # Low risk (recent, converted)
    "uplift_score": 0.42,  # Likely to respond to treatment
    "customer_type": "Persuadable",  # Should be targeted
    "clv_estimate": 2500.0  # Estimated lifetime value
}
```

---

## Troubleshooting

### Error: "Missing required column"

**Solution:** Ensure your CSV has the required columns for the selected dataset type.

### Error: "Unable to normalize units"

**Solution:** Check that numeric columns contain valid numbers, not strings or nulls.

### Warning: "Using default values for missing columns"

**Info:** This is normal. The system fills in intelligent defaults for optional fields.

### Issue: All customers have similar RFM scores

**Solution:** Your data may lack variation. Ensure you have diverse customer behavior in the dataset.

---

## Next Steps

1. **Download Real Datasets:**
   ```bash
   cd backend
   python scripts/download_real_datasets.py
   ```

2. **Upload via UI or API:**
   - UI: http://localhost:5173/behavior-analysis
   - API: See SETUP_AND_RUN_GUIDE.md

3. **Verify Normalization:**
   - Check dataset statistics endpoint
   - Review customer behavior summaries
   - Inspect RFM segment distribution

4. **Analyze Results:**
   - Get high-risk customers
   - View personalized interventions
   - Calculate expected ROI
