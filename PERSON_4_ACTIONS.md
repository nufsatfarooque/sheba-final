# 👤 PERSON 4: WIDGET + DEMO ENGINEER
## Complete Action Plan (8-10 Hours for 27-30 Hour Hackathon)

---

## 🎯 Your Mission
You are the **customer-facing storyteller**. While backend/frontend handle B2B operations, you build:
1. **Widget** - Embeddable JS that any customer can integrate
2. **Demo Site** - Fake customer portal showing the widget in action
3. **Message Preview** - Gallery of all generated save actions
4. **Presentation** - Make the product shine for judges

---

## 📋 Your 4 Main Deliverables

### 1️⃣ **Customer Widget (2-3 hours)**
### 2️⃣ **Demo Site & Embedding (2-3 hours)**
### 3️⃣ **Save Action Preview Page (1-2 hours)**
### 4️⃣ **Demo Flow & Polish (2-3 hours)**

**Total: ~8-11 hours** (leaves buffer for debugging)

---

# 📌 PART 1: CUSTOMER WIDGET (Hours 1-3)

## What is the Widget?
A small, embeddable JavaScript component that customers (B2B2C) see on your SaaS dashboard.

**Example of where it appears:**
```
Customer Portal (Telecom, E-commerce, SaaS, etc.)
┌─────────────────────────────────┐
│ Welcome to Acme Customer Portal  │
│ ┌─────────────────────────────┐ │
│ │  SHEBA WIDGET (embeds here) │ │
│ │                             │ │
│ │  Hi, Acme Corp!             │ │
│ │  Your Loyalty: ⭐⭐⭐⭐⭐  │ │
│ │  We'd love to keep you!     │ │
│ │  [View Your Offer] [Claim]  │ │
│ │                             │ │
│ └─────────────────────────────┘ │
│                                 │
│ (rest of portal...)             │
└─────────────────────────────────┘
```

---

## Step 1A: Create Widget File

Create a new file in the **frontend** folder:

```bash
frontend/src/widgets/sheba-widget.js
```

**Content:**

```javascript
// sheba-widget.js
// Embeddable Sheba Widget for Customer Portals

(function() {
  const WIDGET_CSS = `
    .sheba-widget {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 400px;
      padding: 20px;
      border-radius: 12px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
      margin: 20px 0;
    }
    
    .sheba-widget h3 {
      margin: 0 0 10px 0;
      font-size: 18px;
      font-weight: 600;
    }
    
    .sheba-widget-stat {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin: 10px 0;
      font-size: 14px;
    }
    
    .sheba-widget-score {
      font-size: 32px;
      font-weight: bold;
    }
    
    .sheba-widget-badge {
      display: inline-block;
      padding: 4px 12px;
      background: rgba(255,255,255,0.2);
      border-radius: 20px;
      font-size: 12px;
      margin: 5px 0;
    }
    
    .sheba-widget-tip {
      margin: 10px 0;
      padding: 10px;
      background: rgba(255,255,255,0.1);
      border-radius: 8px;
      font-size: 13px;
      line-height: 1.4;
    }
    
    .sheba-widget-button {
      display: inline-block;
      margin-top: 15px;
      padding: 10px 20px;
      background: white;
      color: #667eea;
      border: none;
      border-radius: 6px;
      font-weight: 600;
      cursor: pointer;
      font-size: 14px;
      transition: transform 0.2s;
    }
    
    .sheba-widget-button:hover {
      transform: scale(1.05);
    }
    
    .sheba-widget-loading {
      text-align: center;
      padding: 20px;
      font-size: 14px;
    }
    
    .sheba-widget-error {
      background: #ef4444;
      padding: 15px;
      border-radius: 8px;
      font-size: 13px;
    }
  `;

  window.ShebaWidget = {
    version: '1.0.0',
    
    init: async function(config) {
      // config = { org_api_key, customer_id, container_id, api_url }
      
      if (!config.org_api_key || !config.customer_id) {
        console.error('ShebaWidget: Missing org_api_key or customer_id');
        return;
      }
      
      const container = document.getElementById(config.container_id || 'sheba-widget');
      if (!container) {
        console.error('ShebaWidget: Container not found');
        return;
      }
      
      // Inject CSS
      const style = document.createElement('style');
      style.textContent = WIDGET_CSS;
      document.head.appendChild(style);
      
      // Show loading
      container.innerHTML = '<div class="sheba-widget sheba-widget-loading">Loading...</div>';
      
      try {
        // Fetch widget data from backend
        const api_url = config.api_url || 'http://localhost:8000';
        const response = await fetch(
          `${api_url}/api/v1/widget/customer_view?api_key=${config.org_api_key}&customer_id=${config.customer_id}`
        );
        
        if (!response.ok) throw new Error('Failed to fetch widget data');
        
        const data = await response.json();
        
        // Render widget
        const html = `
          <div class="sheba-widget">
            <h3>👋 Hi, ${data.customer_name}!</h3>
            
            <div class="sheba-widget-stat">
              <span>Your Loyalty Score</span>
              <span class="sheba-widget-score">${data.loyalty_score}/10</span>
            </div>
            
            <div class="sheba-widget-stat">
              <span>Engagement Level</span>
              <span class="sheba-widget-badge">${data.engagement_level}</span>
            </div>
            
            <p style="margin: 12px 0; font-size: 14px;">${data.risk_message}</p>
            
            <div style="margin: 10px 0;">
              <strong>🎁 Special Offer:</strong>
              <div class="sheba-widget-badge" style="display: block;">${data.recommended_offer}</div>
            </div>
            
            ${data.tips.map(tip => `<div class="sheba-widget-tip">💡 ${tip}</div>`).join('')}
            
            <button class="sheba-widget-button" onclick="window.ShebaWidget.claimOffer('${config.customer_id}')">
              Claim Now
            </button>
          </div>
        `;
        
        container.innerHTML = html;
        
      } catch (error) {
        console.error('ShebaWidget Error:', error);
        container.innerHTML = `
          <div class="sheba-widget sheba-widget-error">
            ⚠️ Unable to load widget. Please refresh.
          </div>
        `;
      }
    },
    
    claimOffer: function(customerId) {
      console.log(`Offer claimed for customer: ${customerId}`);
      alert('Thank you! Your offer has been claimed. Check your email.');
      // In real version, would post to backend
    }
  };
  
  console.log('ShebaWidget v' + window.ShebaWidget.version + ' loaded');
})();
```

---

## Step 1B: Create Widget Documentation File

```bash
frontend/public/sheba-widget-guide.html
```

**Content:**

```html
<!DOCTYPE html>
<html>
<head>
  <title>Sheba Widget Integration Guide</title>
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      max-width: 900px;
      margin: 0 auto;
      padding: 40px 20px;
      background: #f5f5f5;
    }
    .container {
      background: white;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    h1 { color: #667eea; }
    .code-block {
      background: #2d2d2d;
      color: #f8f8f2;
      padding: 15px;
      border-radius: 8px;
      overflow-x: auto;
      font-family: 'Courier New', monospace;
      font-size: 13px;
      margin: 15px 0;
    }
    .step { margin: 30px 0; }
    .step h3 { color: #667eea; }
  </style>
</head>
<body>
  <div class="container">
    <h1>🎨 Sheba Widget Integration Guide</h1>
    
    <div class="step">
      <h3>Step 1: Add Script Tag</h3>
      <p>Add this to your customer portal:</p>
      <div class="code-block">
&lt;script src="https://your-domain.com/sheba-widget.js"&gt;&lt;/script&gt;
      </div>
    </div>
    
    <div class="step">
      <h3>Step 2: Create Container</h3>
      <div class="code-block">
&lt;div id="sheba-widget"&gt;&lt;/div&gt;
      </div>
    </div>
    
    <div class="step">
      <h3>Step 3: Initialize Widget</h3>
      <div class="code-block">
&lt;script&gt;
  window.ShebaWidget.init({
    org_api_key: "pk_live_YOUR_KEY_HERE",
    customer_id: "cust_acme_001",
    container_id: "sheba-widget",
    api_url: "https://sheba-api.example.com"
  });
&lt;/script&gt;
      </div>
    </div>
    
    <div class="step">
      <h3>Full Example</h3>
      <div class="code-block">
&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;title&gt;My Customer Portal&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
  &lt;h1&gt;Welcome to Your Portal&lt;/h1&gt;
  
  &lt;!-- Sheba Widget --&gt;
  &lt;div id="sheba-widget"&gt;&lt;/div&gt;
  
  &lt;script src="https://sheba-api.example.com/sheba-widget.js"&gt;&lt;/script&gt;
  &lt;script&gt;
    ShebaWidget.init({
      org_api_key: "pk_live_demo123",
      customer_id: "customer_456",
      container_id: "sheba-widget",
      api_url: "https://sheba-api.example.com"
    });
  &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;
      </div>
    </div>
    
    <h2>Configuration Options</h2>
    <table style="width: 100%; border-collapse: collapse;">
      <tr style="background: #f0f0f0;">
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Property</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Required</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Description</strong></td>
      </tr>
      <tr>
        <td style="padding: 10px; border: 1px solid #ddd;">org_api_key</td>
        <td style="padding: 10px; border: 1px solid #ddd;">✓</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Your organization's API key</td>
      </tr>
      <tr>
        <td style="padding: 10px; border: 1px solid #ddd;">customer_id</td>
        <td style="padding: 10px; border: 1px solid #ddd;">✓</td>
        <td style="padding: 10px; border: 1px solid #ddd;">Unique customer identifier</td>
      </tr>
      <tr>
        <td style="padding: 10px; border: 1px solid #ddd;">container_id</td>
        <td style="padding: 10px; border: 1px solid #ddd;">✓</td>
        <td style="padding: 10px; border: 1px solid #ddd;">ID of HTML element to render widget</td>
      </tr>
      <tr>
        <td style="padding: 10px; border: 1px solid #ddd;">api_url</td>
        <td style="padding: 10px; border: 1px solid #ddd;"></td>
        <td style="padding: 10px; border: 1px solid #ddd;">Sheba backend URL (default: localhost:8000)</td>
      </tr>
    </table>
  </div>
</body>
</html>
```

---

## Step 1C: Add Widget to Frontend Vite

Update `frontend/vite.config.js` to expose the widget:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
  build: {
    rollupOptions: {
      output: {
        // Widget builds as standalone JS
      }
    }
  }
})
```

Create `frontend/src/widgets/build-widget.js`:

```javascript
// Script to build standalone widget
// Run: node build-widget.js

const fs = require('fs');
const path = require('path');

const widgetCode = fs.readFileSync(
  path.join(__dirname, 'sheba-widget.js'),
  'utf-8'
);

const output = `
// Sheba Widget v1.0.0
// Embeddable customer engagement widget
${widgetCode}
`;

fs.writeFileSync(
  path.join(__dirname, '../../public/dist/sheba-widget.js'),
  output
);

console.log('✅ Widget built: public/dist/sheba-widget.js');
```

---

# 📌 PART 2: DEMO SITE & EMBEDDING (Hours 4-6)

## What is the Demo Site?

A fake customer portal showing how customers experience the widget + your retention messages.

**Example:** "Acme Telecom Customer Portal" with widget embedded

---

## Step 2A: Create Demo Site Page

Create `frontend/src/pages/DemoSite.jsx`:

```jsx
import React, { useEffect } from 'react';

export default function DemoSite() {
  useEffect(() => {
    // Load widget script
    const script = document.createElement('script');
    script.src = 'http://localhost:5173/sheba-widget.js';
    script.async = true;
    document.body.appendChild(script);
    
    // Initialize after script loads
    script.onload = () => {
      window.ShebaWidget?.init({
        org_api_key: 'pk_live_demo123',
        customer_id: 'cust_acme_corp',
        container_id: 'sheba-widget-container',
        api_url: 'http://localhost:8000'
      });
    };
  }, []);
  
  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <div style={styles.headerContent}>
          <h1>Acme Corp Portal</h1>
          <p>Customer Service Dashboard</p>
        </div>
        <div style={styles.userProfile}>
          <span>Logged in: John Doe</span>
          <button style={styles.logoutBtn}>Logout</button>
        </div>
      </header>
      
      <div style={styles.container}>
        <nav style={styles.sidebar}>
          <ul>
            <li><a href="#dashboard">Dashboard</a></li>
            <li><a href="#billing">Billing</a></li>
            <li><a href="#support">Support</a></li>
            <li><a href="#settings">Settings</a></li>
          </ul>
        </nav>
        
        <main style={styles.main}>
          <h2>Welcome Back, John!</h2>
          <p>Here's your account overview.</p>
          
          {/* Widget Container */}
          <div id="sheba-widget-container"></div>
          
          <div style={styles.cardGrid}>
            <div style={styles.card}>
              <h3>📊 Usage This Month</h3>
              <p style={styles.cardValue}>2,450 GB</p>
            </div>
            <div style={styles.card}>
              <h3>💰 Current Bill</h3>
              <p style={styles.cardValue}>$199.99</p>
            </div>
            <div style={styles.card}>
              <h3>🎯 Account Status</h3>
              <p style={styles.cardValue}>Active</p>
            </div>
          </div>
          
          <div style={styles.recentActivity}>
            <h3>Recent Activity</h3>
            <ul>
              <li>✅ Payment processed - Dec 1</li>
              <li>📧 Invoice sent - Dec 1</li>
              <li>🔄 Plan renewed - Nov 1</li>
            </ul>
          </div>
        </main>
      </div>
      
      <footer style={styles.footer}>
        <p>© 2025 Acme Corp. All rights reserved.</p>
      </footer>
    </div>
  );
}

const styles = {
  page: {
    minHeight: '100vh',
    background: '#f5f5f5',
    display: 'flex',
    flexDirection: 'column',
  },
  header: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    padding: '20px 40px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerContent: {
    flex: 1,
  },
  userProfile: {
    display: 'flex',
    gap: '15px',
    alignItems: 'center',
  },
  logoutBtn: {
    background: 'white',
    color: '#667eea',
    border: 'none',
    padding: '8px 16px',
    borderRadius: '6px',
    cursor: 'pointer',
    fontWeight: 600,
  },
  container: {
    display: 'flex',
    flex: 1,
  },
  sidebar: {
    width: '200px',
    background: 'white',
    padding: '20px',
    borderRight: '1px solid #e0e0e0',
  },
  main: {
    flex: 1,
    padding: '40px',
  },
  cardGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '20px',
    margin: '30px 0',
  },
  card: {
    background: 'white',
    padding: '20px',
    borderRadius: '12px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    textAlign: 'center',
  },
  cardValue: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#667eea',
    margin: '10px 0 0 0',
  },
  recentActivity: {
    background: 'white',
    padding: '20px',
    borderRadius: '12px',
    marginTop: '30px',
  },
  footer: {
    background: '#333',
    color: 'white',
    textAlign: 'center',
    padding: '20px',
    marginTop: 'auto',
  },
};
```

---

## Step 2B: Add Route to App

Update `frontend/src/App.jsx`:

```jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DemoSite from './pages/DemoSite';

function App() {
  return (
    <Router>
      <Routes>
        {/* Existing routes */}
        <Route path="/demo" element={<DemoSite />} />
      </Routes>
    </Router>
  );
}

export default App;
```

---

# 📌 PART 3: SAVE ACTION PREVIEW PAGE (Hours 7-8)

This page shows all the personalized emails/SMS messages your system generated.

---

## Step 3A: Create Save Action Gallery

Create `frontend/src/pages/SaveActionGallery.jsx`:

```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function SaveActionGallery() {
  const [actions, setActions] = useState([]);
  const [selectedAction, setSelectedAction] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchSaveActions();
  }, []);
  
  const fetchSaveActions = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/save-actions', {
        params: { org_id: 'demo_org' }
      });
      setActions(response.data.actions || []);
    } catch (error) {
      console.error('Error fetching save actions:', error);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) return <div style={styles.center}>Loading...</div>;
  
  return (
    <div style={styles.container}>
      <h1>🚀 Generated Save Actions</h1>
      <p style={styles.subtitle}>
        Personalized messages that auto-saved your customers
      </p>
      
      <div style={styles.stats}>
        <div style={styles.stat}>
          <div style={styles.statNumber}>{actions.length}</div>
          <div style={styles.statLabel}>Messages Generated</div>
        </div>
        <div style={styles.stat}>
          <div style={styles.statNumber}>
            ${actions.reduce((sum, a) => sum + (a.projected_saved || 0), 0).toLocaleString()}
          </div>
          <div style={styles.statLabel}>Revenue Projected to Save</div>
        </div>
      </div>
      
      <div style={styles.gallery}>
        {actions.map((action, idx) => (
          <div
            key={idx}
            style={{
              ...styles.card,
              borderLeft: `4px solid ${selectedAction?.customer_id === action.customer_id ? '#667eea' : '#e0e0e0'}`,
              cursor: 'pointer',
              background: selectedAction?.customer_id === action.customer_id ? '#f0f4ff' : 'white',
            }}
            onClick={() => setSelectedAction(action)}
          >
            <div style={styles.cardHeader}>
              <h3>{action.customer_name}</h3>
              <span style={styles.badge}>
                Risk: {Math.round(action.churn_score * 100)}%
              </span>
            </div>
            <p style={styles.cardMeta}>
              Revenue at Risk: <strong>${action.revenue_at_risk.toLocaleString()}</strong>
            </p>
            <p style={styles.cardMeta}>
              Projected Save: <strong>${action.projected_saved.toLocaleString()}</strong>
            </p>
          </div>
        ))}
      </div>
      
      {selectedAction && (
        <div style={styles.previewPanel}>
          <h2>Message Preview</h2>
          
          <div style={styles.previewSection}>
            <h3>📧 Email</h3>
            <div style={styles.emailPreview}>
              <div style={styles.emailField}>
                <strong>Subject:</strong> {selectedAction.email.subject}
              </div>
              <div style={styles.emailBody}>
                {selectedAction.email.body}
              </div>
            </div>
          </div>
          
          <div style={styles.previewSection}>
            <h3>💬 SMS</h3>
            <div style={styles.smsPreview}>
              {selectedAction.sms.message}
            </div>
          </div>
          
          <div style={styles.previewSection}>
            <h3>💰 Impact</h3>
            <div style={styles.impactBox}>
              <div>Revenue at Risk: <strong>${selectedAction.revenue_at_risk.toLocaleString()}</strong></div>
              <div style={{marginTop: '10px'}}>
                If this customer stays: <strong style={{color: '#22c55e'}}>
                  +${selectedAction.projected_saved.toLocaleString()}
                </strong>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '40px 20px',
  },
  subtitle: {
    fontSize: '16px',
    color: '#666',
    marginBottom: '30px',
  },
  stats: {
    display: 'grid',
    gridTemplateColumns: 'repeat(2, 1fr)',
    gap: '20px',
    marginBottom: '40px',
  },
  stat: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    padding: '30px',
    borderRadius: '12px',
    textAlign: 'center',
  },
  statNumber: {
    fontSize: '40px',
    fontWeight: 'bold',
    marginBottom: '10px',
  },
  statLabel: {
    fontSize: '14px',
    opacity: 0.9,
  },
  gallery: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '20px',
    marginBottom: '40px',
  },
  card: {
    background: 'white',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    transition: 'all 0.3s',
  },
  cardHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '12px',
  },
  badge: {
    background: '#fee',
    color: '#c00',
    padding: '4px 12px',
    borderRadius: '20px',
    fontSize: '12px',
    fontWeight: 600,
  },
  cardMeta: {
    fontSize: '14px',
    color: '#666',
    margin: '8px 0',
  },
  previewPanel: {
    background: 'white',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
  },
  previewSection: {
    marginBottom: '30px',
    paddingBottom: '20px',
    borderBottom: '1px solid #e0e0e0',
  },
  emailPreview: {
    background: '#f5f5f5',
    padding: '20px',
    borderRadius: '8px',
    fontFamily: 'monospace',
  },
  emailField: {
    marginBottom: '15px',
    fontSize: '14px',
  },
  emailBody: {
    whiteSpace: 'pre-wrap',
    lineHeight: '1.6',
    fontSize: '13px',
  },
  smsPreview: {
    background: '#e8f5e9',
    padding: '20px',
    borderRadius: '8px',
    fontSize: '14px',
    lineHeight: '1.6',
    fontFamily: 'monospace',
  },
  impactBox: {
    background: '#f0f4ff',
    padding: '20px',
    borderRadius: '8px',
    fontSize: '14px',
    lineHeight: '1.8',
  },
  center: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    fontSize: '18px',
    color: '#666',
  },
};
```

---

## Step 3B: Add Route

Update `frontend/src/App.jsx`:

```jsx
import SaveActionGallery from './pages/SaveActionGallery';

<Route path="/save-actions" element={<SaveActionGallery />} />
```

---

# 📌 PART 4: DEMO FLOW & POLISH (Hours 9-11)

This is about making a compelling story for judges.

---

## Step 4A: Create Demo Narrative Page

Create `frontend/src/pages/DemoNarrative.jsx`:

```jsx
import React, { useState } from 'react';

export default function DemoNarrative() {
  const [step, setStep] = useState(0);
  
  const steps = [
    {
      title: '📊 Step 1: Upload Customer Data',
      description: 'Telecom company uploads their customer database (1,000 customers)',
      action: 'Upload Sample CSV',
      link: '/upload',
      visual: 'CSV file icon → Processing bar → ✅ Success'
    },
    {
      title: '🎯 Step 2: System Analyzes Churn Risk',
      description: 'Our ML engine instantly identifies 150 high-risk customers',
      action: 'View Overview Dashboard',
      link: '/dashboard',
      visual: 'Pie chart showing risk distribution, customer table'
    },
    {
      title: '💰 Step 3: Retention ROI Calculation',
      description: 'System calculates: $500K revenue at risk, potential $150K save',
      action: 'See ROI Dashboard',
      link: '/dashboard/roi',
      visual: 'Large numbers + projected savings'
    },
    {
      title: '🚀 Step 4: Generate Save Actions',
      description: 'System auto-generates personalized emails + SMS for top 10%',
      action: 'View Generated Messages',
      link: '/save-actions',
      visual: 'Gallery of 15 personalized messages'
    },
    {
      title: '🎨 Step 5: Widget Integration',
      description: 'Customers see engagement tips on their portal',
      action: 'See Widget in Action',
      link: '/demo',
      visual: 'Live widget demo embedded'
    },
    {
      title: '📈 The Impact',
      description: '✅ 150 at-risk customers engaged\n✅ $150K revenue protected\n✅ Auto-escalation saves 5 hours',
      action: 'Ready to Deploy!',
      link: '#',
      visual: 'Green checkmarks + success metrics'
    }
  ];
  
  const current = steps[step];
  
  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <div style={styles.progressBar}>
          <div style={{
            ...styles.progress,
            width: `${((step + 1) / steps.length) * 100}%`
          }}></div>
        </div>
        
        <h1 style={styles.title}>{current.title}</h1>
        <p style={styles.description}>{current.description}</p>
        
        <div style={styles.visual}>
          {current.visual}
        </div>
        
        <div style={styles.actions}>
          <button
            onClick={() => setStep(Math.max(0, step - 1))}
            disabled={step === 0}
            style={{...styles.btn, ...styles.btnSecondary, opacity: step === 0 ? 0.5 : 1}}
          >
            ← Previous
          </button>
          
          {current.link !== '#' && (
            <a href={current.link} style={styles.btnPrimary}>
              {current.action} →
            </a>
          )}
          
          <button
            onClick={() => setStep(Math.min(steps.length - 1, step + 1))}
            disabled={step === steps.length - 1}
            style={{...styles.btn, opacity: step === steps.length - 1 ? 0.5 : 1}}
          >
            Next →
          </button>
        </div>
        
        <div style={styles.dots}>
          {steps.map((_, idx) => (
            <div
              key={idx}
              onClick={() => setStep(idx)}
              style={{
                ...styles.dot,
                background: idx <= step ? '#667eea' : '#e0e0e0',
              }}
            ></div>
          ))}
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    display: 'flex',
    alignItems: 'center',
    padding: '40px 20px',
  },
  container: {
    maxWidth: '600px',
    background: 'white',
    borderRadius: '20px',
    padding: '50px 40px',
    boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
  },
  progressBar: {
    height: '6px',
    background: '#e0e0e0',
    borderRadius: '3px',
    marginBottom: '30px',
    overflow: 'hidden',
  },
  progress: {
    height: '100%',
    background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
    transition: 'width 0.3s ease',
  },
  title: {
    fontSize: '28px',
    marginBottom: '15px',
    color: '#333',
  },
  description: {
    fontSize: '16px',
    color: '#666',
    lineHeight: '1.6',
    marginBottom: '30px',
  },
  visual: {
    background: '#f5f5f5',
    padding: '40px',
    borderRadius: '12px',
    textAlign: 'center',
    fontSize: '18px',
    fontWeight: 600,
    color: '#667eea',
    marginBottom: '30px',
    minHeight: '100px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: 'monospace',
  },
  actions: {
    display: 'flex',
    gap: '12px',
    marginBottom: '20px',
  },
  btn: {
    padding: '12px 24px',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: 600,
    cursor: 'pointer',
    transition: 'all 0.3s',
    flex: 1,
  },
  btnSecondary: {
    background: '#e0e0e0',
    color: '#333',
  },
  btnPrimary: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    padding: '12px 24px',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: 600',
    textDecoration: 'none',
    flex: 1,
    textAlign: 'center',
    transition: 'transform 0.3s',
  },
  dots: {
    display: 'flex',
    gap: '8px',
    justifyContent: 'center',
  },
  dot: {
    width: '12px',
    height: '12px',
    borderRadius: '50%',
    cursor: 'pointer',
    transition: 'background 0.3s',
  },
};
```

---

## Step 4B: Create Presentation Checklist

Create `DEMO_PRESENTATION_CHECKLIST.md`:

```markdown
# 🎤 Demo Presentation Checklist (For Judges)

## Opening (1 min)
- [ ] "We built SHEBA - automated churn prediction + retention for B2B"
- [ ] Show 1-sentence value prop: "150 at-risk customers identified in seconds, $150K revenue saved"

## Live Demo (5-7 min)
- [ ] Go to `/upload` → Upload sample CSV
- [ ] Show success message + initial stats
- [ ] Go to `/dashboard` → Show churn overview
  - Highlight: "150 high-risk customers detected"
  - Show: Risk distribution pie chart
- [ ] Go to `/dashboard/roi` → Show retention ROI
  - Highlight: "$500K revenue at risk, $150K projected saved"
- [ ] Go to `/save-actions` → Show generated messages
  - Click one to see: Personalized email + SMS preview
  - Highlight: "Each message auto-generated, takes <1 second"
- [ ] Go to `/demo` → Show widget embedded
  - Explain: "Customers see engagement tips + personalized offers"

## Architecture (2-3 min)
- [ ] Show ARCHITECTURE.md diagram
- [ ] Explain: ML engine → Backend APIs → Frontend + Widget
- [ ] Key point: "Generalizable - works with ANY org's data"

## Competitive Advantage (1 min)
- [ ] ✅ End-to-end churn platform (not just prediction)
- [ ] ✅ Auto-generates personalized retention actions
- [ ] ✅ B2B + B2B2C (operators + customers)
- [ ] ✅ ROI-focused dashboard
- [ ] ✅ Works with any data format

## Closing (30 sec)
- [ ] "30-hour hackathon build"
- [ ] "Production-ready for telcos, SaaS, e-commerce"
- [ ] "Questions?"

## Before You Demo
- [ ] Test upload with sample data
- [ ] Verify backend is running (port 8000)
- [ ] Verify frontend is running (port 5173)
- [ ] Have screenshot backups in case of connection issues
- [ ] Practice timing (keep to <10 min total)
```

---

# ✅ YOUR COMPLETE CHECKLIST

**Hours 0-1**: Set up widget file + documentation  
**Hours 1-3**: Widget JS complete and working  
**Hours 3-5**: Demo site with portal + embedded widget  
**Hours 5-7**: Save action preview gallery  
**Hours 7-9**: Demo narrative page + polish  
**Hours 9-10**: Testing + final touches  
**Hours 10-11**: Presentation prep + backup screenshots  

---

# 🚀 FINAL DELIVERABLES (You're Responsible For)

1. ✅ **sheba-widget.js** - Embeddable customer widget
2. ✅ **Widget Integration Guide** - How to embed on any site
3. ✅ **DemoSite.jsx** - Fake Acme telecom portal with widget
4. ✅ **SaveActionGallery.jsx** - Gallery of personalized messages
5. ✅ **DemoNarrative.jsx** - Step-by-step demo flow
6. ✅ **Demo Presentation Checklist** - Judge-facing story
7. ✅ **Public widget files** - `public/sheba-widget.js` + docs

---

# 🎯 Success Criteria

✅ **Widget loads** on demo site without errors  
✅ **Messages gallery** shows real data from backend  
✅ **Demo flow** is smooth and compelling  
✅ **Story is clear** - judges understand the B2B2C value  
✅ **Backup plan** - screenshots ready if network fails  

---

Now start building! You've got this. 💪

Questions as you go? Ask the backend/frontend team anytime.
```

