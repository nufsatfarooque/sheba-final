# 🏗️ SHEBA - Churn Prediction & Retention Platform
## Professional Architecture & System Design (Hackathon Edition)

---

## 📊 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CUSTOMER ORGANIZATIONS                              │
└────────────────┬────────────────────────────────────┬──────────────────────┘
                 │                                    │
         ┌───────▼────────┐               ┌──────────▼────────┐
         │  CSV Upload    │               │  Widget Script    │
         │   (B2B Side)   │               │  (B2B2C Side)     │
         └────────┬───────┘               └─────────┬─────────┘
                  │                                 │
                  │                    ┌────────────┴────────────┐
                  │                    │                         │
         ┌────────▼────────────────────▼──────┐        ┌────────▼──────┐
         │   SHEBA BACKEND (FastAPI)          │        │ Customer Site │
         │  ┌──────────────────────────────┐  │        │   Portal      │
         │  │ API Layer                    │  │        │               │
         │  │ • /upload/csv                │  │        │  Embeds:      │
         │  │ • /churn/overview            │  │        │  • Widget JS  │
         │  │ • /retention/roi             │  │        │  • Shows risk │
         │  │ • /segments/summary          │  │        │  • Shows tips │
         │  │ • /postmortem/insights       │  │        └───────────────┘
         │  │ • /customers/{id}            │  │
         │  │ • /save-action/generate      │  │
         │  │ • /widget/customer_view      │  │
         │  └────────────┬─────────────────┘  │
         │               │                    │
         │  ┌────────────▼──────────────────┐ │
         │  │ Business Logic Layer          │ │
         │  │ • Data ingestion              │ │
         │  │ • Call ML functions           │ │
         │  │ • Generate save actions       │ │
         │  │ • Aggregate metrics           │ │
         │  └────────────┬──────────────────┘ │
         │               │                    │
         │  ┌────────────▼──────────────────┐ │
         │  │ Data Layer (PostgreSQL)       │ │
         │  │ • Organizations               │ │
         │  │ • Customers                   │ │
         │  │ • Transactions/Events         │ │
         │  │ • Churn Scores & Segments     │ │
         │  │ • Generated Messages          │ │
         │  │ • Analytics Cache             │ │
         │  └───────────────────────────────┘ │
         └────────────────────────────────────┘
                  │
         ┌────────▼─────────────────┐
         │  ML/DATA ENGINE           │
         │  (Python Module)          │
         │  ┌─────────────────────┐  │
         │  │ Feature Engineering │  │
         │  │ • RFM metrics       │  │
         │  │ • Activity trends   │  │
         │  └─────────────────────┘  │
         │  ┌─────────────────────┐  │
         │  │ Churn Prediction    │  │
         │  │ • Rule-based scorer │  │
         │  │ • Risk classification   │
         │  └─────────────────────┘  │
         │  ┌─────────────────────┐  │
         │  │ Analytics Functions │  │
         │  │ • Segmentation      │  │
         │  │ • Value calculation │  │
         │  │ • ROI estimation    │  │
         │  │ • Postmortem rules  │  │
         │  └─────────────────────┘  │
         └──────────────────────────┘
                  │
         ┌────────▼──────────────┐
         │  FRONTEND (React+Vite)│
         │  ┌──────────────────┐ │
         │  │ B2B Dashboard    │ │
         │  │ • Upload page    │ │
         │  │ • Churn overview │ │
         │  │ • ROI dashboard  │ │
         │  │ • Customer detail│ │
         │  │ • Postmortem     │ │
         │  └──────────────────┘ │
         │  ┌──────────────────┐ │
         │  │ Widget Builder   │ │
         │  │ • Preview widget │ │
         │  │ • Generate code  │ │
         │  └──────────────────┘ │
         │  ┌──────────────────┐ │
         │  │ Demo Site        │ │
         │  │ • Sample portal  │ │
         │  │ • Embedded widget│ │
         │  └──────────────────┘ │
         └──────────────────────┘

```

---

## 📦 Component Dependencies & Data Flow

```
UPLOAD FLOW (Day 1: Data Ingestion)
═════════════════════════════════════
User CSV  →  Backend /upload  →  Parse & Validate  →  ML Engine
                                                      ↓
                                        Compute features (RFM, trends)
                                                      ↓
                                        Churn scoring & segmentation
                                                      ↓
                                        Save to DB (Customers table)
                                                      ↓
                                        Return: import_id, stats


DASHBOARD FLOW (Day 2: Analysis & Insights)
═════════════════════════════════════════════
Dashboard  →  Backend /churn/overview  →  Query DB  →  Get scores
                                                      ↓
                                          Filter & aggregate
                                                      ↓
                                          Return JSON (KPIs, table)
                                                      ↓
                                          Frontend renders charts


SAVE ACTION FLOW (Day 3: Retention Actions)
════════════════════════════════════════════
User clicks "Save Customer" → Backend /save-action/generate
                                        ↓
                                Call ML postmortem (predict reason)
                                        ↓
                                Generate personalized message
                                        ↓
                                Estimate revenue saved (LTV × risk%)
                                        ↓
                                Store in DB & return preview
                                        ↓
                                Frontend shows email/SMS modal


WIDGET FLOW (Day 3: Customer-Facing Integration)
═════════════════════════════════════════════════
Customer Site  →  Embed widget.js  →  Calls /widget/customer_view
                                              ↓
                                        Backend queries customer risk
                                              ↓
                                        Returns simplified view
                                              ↓
                                        Widget renders in iframe/DOM
```

---

## 🗄️ Database Schema (PostgreSQL)

```sql
-- Organizations (multi-tenant)
CREATE TABLE organizations (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    created_at TIMESTAMP,
    api_key VARCHAR(255) UNIQUE
);

-- Customers
CREATE TABLE customers (
    id UUID PRIMARY KEY,
    org_id UUID REFERENCES organizations,
    customer_id VARCHAR(255),  -- Client's own ID
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    total_revenue DECIMAL(12,2),
    last_transaction_date DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- RFM & Features (computed)
CREATE TABLE customer_features (
    id UUID PRIMARY KEY,
    customer_id UUID REFERENCES customers,
    recency INT,  -- days since last purchase
    frequency INT,  -- number of transactions
    monetary DECIMAL(12,2),  -- total spend
    churn_score FLOAT,  -- 0.0 to 1.0
    churn_risk VARCHAR(50),  -- 'high', 'medium', 'low'
    segment VARCHAR(50),  -- 'loyal', 'at-risk', 'new', 'dormant'
    customer_value DECIMAL(12,2),  -- LTV estimate
    computed_at TIMESTAMP
);

-- Transactions (for feature calc)
CREATE TABLE transactions (
    id UUID PRIMARY KEY,
    customer_id UUID REFERENCES customers,
    amount DECIMAL(12,2),
    transaction_date DATE,
    created_at TIMESTAMP
);

-- Generated Save Actions
CREATE TABLE save_actions (
    id UUID PRIMARY KEY,
    customer_id UUID REFERENCES customers,
    email_subject TEXT,
    email_body TEXT,
    sms_message TEXT,
    revenue_at_risk DECIMAL(12,2),
    projected_saved DECIMAL(12,2),
    generated_at TIMESTAMP,
    status VARCHAR(50)  -- 'generated', 'sent', 'rejected'
);

-- Analytics Cache
CREATE TABLE analytics_cache (
    id UUID PRIMARY KEY,
    org_id UUID REFERENCES organizations,
    metric_type VARCHAR(100),  -- 'churn_overview', 'roi_summary', etc.
    data JSONB,  -- Cached result
    cached_at TIMESTAMP,
    expires_at TIMESTAMP
);
```

---

## 🧠 ML Engine Functions (Person 1: Data/ML)

```python
# analysis_engine.py

def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Input: DataFrame with columns [customer_id, date, amount]
    Output: DataFrame with RFM features
    """

def compute_churn_score(features: pd.DataFrame) -> pd.DataFrame:
    """
    Rule-based churn scoring (0.0 = loyal, 1.0 = high churn risk)
    Rules:
    - If recency > 60 days: +0.3
    - If frequency < 2 in last 6m: +0.3
    - If monetary declining: +0.2
    """

def segment_customers(features: pd.DataFrame) -> pd.Series:
    """
    RFM-based segmentation:
    - 'Loyal': High R, F, M
    - 'At-Risk': Low F or low R, high M
    - 'Dormant': Low R, low F, low M
    - 'New': Recent only
    """

def calculate_customer_value(features: pd.DataFrame) -> pd.Series:
    """
    LTV estimation (simplified):
    - Last 6m avg spend × (1 + predicted lifetime in months) / 12
    """

def postmortem_analysis(churned: pd.DataFrame, retained: pd.DataFrame) -> List[str]:
    """
    Compare churned vs non-churned segments.
    Output:
    [
      "Segment 'Dormant' has 45% churn rate (vs 10% avg)",
      "Customers with 0 transactions in last 40 days churn 5x more"
    ]
    """

def retention_roi(features: pd.DataFrame, top_pct: float = 0.1) -> dict:
    """
    Identify top X% high-risk customers.
    Output:
    {
      "total_revenue_at_risk": 50000,
      "top_10_pct_customers": [cust_ids],
      "projected_saved_at_30pct_retention": 15000
    }
    """
```

---

## 🔌 Backend API Contract (Person 2: Backend)

```
POST /api/v1/upload/csv
────────────────────────
Headers: Authorization: Bearer {token}
Body: FormData with csv file

Response 200:
{
  "import_id": "uuid",
  "stats": {
    "total_customers": 1000,
    "high_risk_count": 150,
    "avg_churn_score": 0.35
  }
}


GET /api/v1/churn/overview
──────────────────────────
Query params: org_id, limit=100

Response 200:
{
  "total_customers": 1000,
  "high_risk_customers": 150,
  "churn_distribution": {
    "high": 150,
    "medium": 250,
    "low": 600
  },
  "customers_table": [
    {
      "id": "cust_123",
      "name": "Acme Corp",
      "risk_score": 0.85,
      "segment": "at-risk",
      "value": 50000,
      "last_activity": "2025-12-01"
    }
  ]
}


GET /api/v1/retention/roi
─────────────────────────
Query params: org_id

Response 200:
{
  "total_revenue_at_risk": 500000,
  "top_10_pct_customers": [
    {
      "id": "cust_456",
      "name": "TechCorp Inc",
      "revenue_at_risk": 75000,
      "churn_score": 0.92
    }
  ],
  "projected_saved_at_30pct_retention": 150000,
  "chart_data": {...}
}


POST /api/v1/save-action/generate
──────────────────────────────────
Body:
{
  "customer_id": "cust_123",
  "org_id": "org_456"
}

Response 200:
{
  "email": {
    "subject": "We'd love to serve Acme Corp better",
    "body": "Hi there! We've noticed...",
    "personalization_score": 0.85
  },
  "sms": {
    "message": "Acme Corp, we have a special offer for you! 20% off..."
  },
  "revenue_at_risk": 50000,
  "projected_saved": 15000,
  "action_id": "action_789"
}


GET /api/v1/widget/customer_view?api_key={key}&customer_id={id}
──────────────────────────────────────────────────────────────
Response 200:
{
  "customer_name": "John Doe",
  "loyalty_score": 7.5,
  "engagement_level": "medium",
  "risk_message": "We value your business!",
  "recommended_offer": "20% off next order",
  "tips": [
    "Your engagement is excellent this month",
    "Referral program could benefit you"
  ]
}


GET /api/v1/postmortem/insights
────────────────────────────────
Query params: org_id

Response 200:
{
  "insights": [
    "Segment 'Dormant' has 45% churn rate (3x average)",
    "Customers with 0 transactions in last 40 days churn 5x more",
    "Average customer lifetime: 18 months"
  ],
  "segment_comparison": {
    "Loyal": { "churn_rate": 5%, "count": 500 },
    "At-Risk": { "churn_rate": 35%, "count": 300 },
    "Dormant": { "churn_rate": 45%, "count": 200 }
  }
}
```

---

## 🎨 Frontend Routes (Person 3: Dashboard)

```
/upload                     → CSV Upload Page
/dashboard                  → Churn Overview Dashboard
/dashboard/customer/:id     → Customer Detail Page
/dashboard/roi              → Retention ROI Dashboard
/dashboard/postmortem       → Postmortem Insights Page
/admin/demo                 → Demo Site Builder
```

---

## 💬 Widget Implementation (Person 4: YOU!)

```javascript
// widget.js - Embed anywhere

<script>
  window.ShebaWidget = {
    init: function(config) {
      // config: { org_api_key, customer_id, container_id }
      // Fetch /api/v1/widget/customer_view
      // Render in iframe or shadow DOM
    }
  };

  // Usage on customer site:
  ShebaWidget.init({
    org_api_key: "pk_live_123456",
    customer_id: "cust_acme_001",
    container_id: "sheba-widget"
  });
</script>

<div id="sheba-widget"></div>
```

---

## ⏰ 30-Hour Timeline (Breakdown by Role)

### Hours 1-6: Setup & Core Foundation
- **ML**: Feature engineering ready
- **Backend**: DB schema, auth middleware
- **Frontend**: Project setup, routing
- **Widget**: Boilerplate & API mocking

### Hours 7-18: Feature Development (Parallel)
- **ML**: Churn scoring, segmentation, value calc
- **Backend**: CSV upload, analytics endpoints
- **Frontend**: Upload page, overview dashboard
- **Widget**: Widget component, demo site

### Hours 19-27: Integration, Polish, Demo
- **ML**: Postmortem, ROI logic finalized
- **Backend**: Save-action endpoint, bug fixes
- **Frontend**: Customer detail, ROI dashboard
- **Widget**: Full integration, presentation polish

### Hours 28-30: Final Demo & Cleanup
- Team rehearsal
- Edge case fixes
- Deck preparation

---

## 🎯 Success Metrics for Judges

✅ **Functional**: Upload CSV → See churn predictions → Generate save action  
✅ **Integrated**: Widget embeds in 3rd party site with real data  
✅ **Polished**: No broken UI, smooth flows  
✅ **Compelling**: ROI numbers + postmortem insights convincing  
✅ **Scalable Story**: Multi-tenant architecture demonstrated  

---

## 🚀 Tech Stack Summary

| Layer | Tech |
|-------|------|
| Frontend | React 19, Vite, Tailwind, Recharts |
| Backend | FastAPI, SQLAlchemy, PostgreSQL |
| ML | Pandas, NumPy, scikit-learn (optional) |
| Widget | Vanilla JS, iframe/shadow DOM |
| Auth | JWT or API key |
| Deployment | Docker (optional for demo) |

