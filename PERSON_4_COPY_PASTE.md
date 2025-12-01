# 🎯 PERSON 4: COPY-PASTE QUICK START

You already have:
✅ Widget file: `frontend/public/sheba-widget.js`
✅ Full documentation: Read `PERSON_4_START_HERE.md`

Now do this in order:

---

## TASK 1: Update App.jsx (5 minutes)

**File**: `frontend/src/App.jsx`

Add these imports at the top:
```jsx
import DemoSite from './pages/DemoSite';
import SaveActionGallery from './pages/SaveActionGallery';
import DemoNarrative from './pages/DemoNarrative';
```

Add these routes inside `<Routes>`:
```jsx
<Route path="/demo" element={<DemoSite />} />
<Route path="/save-actions" element={<SaveActionGallery />} />
<Route path="/demo-narrative" element={<DemoNarrative />} />
```

---

## TASK 2: Create Demo Site Page (1.5 hours)

**File**: Create `frontend/src/pages/DemoSite.jsx`

**Copy this entire content:**

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
          <div id="sheba-widget-container" style={{marginBottom: '30px'}}></div>
          
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

**Test it**: Go to `http://localhost:5173/demo`

---

## TASK 3: Create Messages Gallery (1.5 hours)

**File**: Create `frontend/src/pages/SaveActionGallery.jsx`

**Copy this entire content:**

```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Mock data (use if backend not ready)
const MOCK_ACTIONS = [
  {
    customer_id: "cust_456",
    customer_name: "TechCorp Inc",
    churn_score: 0.92,
    revenue_at_risk: 75000,
    projected_saved: 22500,
    email: {
      subject: "TechCorp, we have something special for you",
      body: "Hi TechCorp Team,\n\nWe've noticed you haven't logged in for 45 days. Your account represents significant value to us, and we'd hate to see you go.\n\nAs a valued customer, we'd like to offer you:\n\n🎁 30% OFF your next 3 months\n🎯 Dedicated account manager\n📞 Priority support\n\nThis offer expires in 7 days. Use code: COMEBACK30\n\nLet's talk about how we can better serve your needs.\n\nBest regards,\nThe Support Team"
    },
    sms: {
      message: "TechCorp - we miss you! 30% off to come back. Use code: COMEBACK30"
    }
  },
  {
    customer_id: "cust_789",
    customer_name: "RetailGo Ltd",
    churn_score: 0.85,
    revenue_at_risk: 45000,
    projected_saved: 13500,
    email: {
      subject: "RetailGo, your loyalty rewards await",
      body: "Hi RetailGo,\n\nYour engagement has been declining, and we want to change that.\n\nAs one of our top customers, you've earned:\n\n🏆 $500 loyalty bonus\n🎁 Free premium features for 1 month\n💰 Referral bonus doubled\n\nClaim your rewards today!\n\nYour Support Team"
    },
    sms: {
      message: "RetailGo: Claim your $500 loyalty bonus! Link: [claim-link]"
    }
  },
  {
    customer_id: "cust_321",
    customer_name: "FinanceFlow",
    churn_score: 0.78,
    revenue_at_risk: 60000,
    projected_saved: 18000,
    email: {
      subject: "We've improved! See what's new for FinanceFlow",
      body: "Hi FinanceFlow Team,\n\nWe've been listening to your feedback and launched new features:\n\n✨ Real-time reporting dashboard\n🔒 Enhanced security protocols\n📊 Custom analytics\n🚀 API integrations\n\nAs an early adopter, get exclusive access + 40% discount.\n\nLet's schedule a demo!\n\nYour Team"
    },
    sms: {
      message: "FinanceFlow: New features available! 40% discount for early adopters. Details: [link]"
    }
  }
];

export default function SaveActionGallery() {
  const [actions, setActions] = useState(MOCK_ACTIONS);
  const [selectedAction, setSelectedAction] = useState(MOCK_ACTIONS[0]);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    // Try to fetch real data, fall back to mock
    fetchSaveActions();
  }, []);
  
  const fetchSaveActions = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:8000/api/v1/save-actions', {
        params: { org_id: 'demo_org' },
        timeout: 3000
      });
      if (response.data.actions) {
        setActions(response.data.actions);
        setSelectedAction(response.data.actions[0]);
      }
    } catch (error) {
      console.log('Using mock data (backend not available)');
      // Use mock data
    } finally {
      setLoading(false);
    }
  };
  
  const totalRevenueSave = actions.reduce((sum, a) => sum + (a.projected_saved || 0), 0);
  
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>🚀 Generated Save Actions</h1>
      <p style={styles.subtitle}>
        Personalized messages that auto-saved your customers
      </p>
      
      <div style={styles.stats}>
        <div style={styles.stat}>
          <div style={styles.statNumber}>{actions.length}</div>
          <div style={styles.statLabel}>Messages Generated</div>
        </div>
        <div style={styles.stat}>
          <div style={styles.statNumber}>${(totalRevenueSave / 1000).toFixed(0)}K</div>
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
              <h3 style={styles.cardTitle}>{action.customer_name}</h3>
              <span style={styles.badge}>
                Risk: {Math.round(action.churn_score * 100)}%
              </span>
            </div>
            <p style={styles.cardMeta}>
              Revenue at Risk: <strong>${action.revenue_at_risk.toLocaleString()}</strong>
            </p>
            <p style={styles.cardMeta}>
              Projected Save: <strong style={{color: '#22c55e'}}>${action.projected_saved.toLocaleString()}</strong>
            </p>
          </div>
        ))}
      </div>
      
      {selectedAction && (
        <div style={styles.previewPanel}>
          <h2 style={styles.previewTitle}>📧 Message Preview: {selectedAction.customer_name}</h2>
          
          <div style={styles.previewSection}>
            <h3 style={styles.sectionTitle}>Email</h3>
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
            <h3 style={styles.sectionTitle}>💬 SMS</h3>
            <div style={styles.smsPreview}>
              {selectedAction.sms.message}
            </div>
          </div>
          
          <div style={styles.previewSection}>
            <h3 style={styles.sectionTitle}>💰 Impact</h3>
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
  title: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '10px',
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
  cardTitle: {
    margin: 0,
    fontSize: '16px',
    fontWeight: 600,
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
  previewTitle: {
    marginTop: 0,
    marginBottom: '20px',
    fontSize: '24px',
    color: '#333',
  },
  previewSection: {
    marginBottom: '30px',
    paddingBottom: '20px',
    borderBottom: '1px solid #e0e0e0',
  },
  sectionTitle: {
    marginTop: 0,
    marginBottom: '12px',
    fontSize: '16px',
    fontWeight: 600,
    color: '#333',
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
    color: '#333',
  },
  smsPreview: {
    background: '#e8f5e9',
    padding: '20px',
    borderRadius: '8px',
    fontSize: '14px',
    lineHeight: '1.6',
    fontFamily: 'monospace',
    color: '#333',
  },
  impactBox: {
    background: '#f0f4ff',
    padding: '20px',
    borderRadius: '8px',
    fontSize: '14px',
    lineHeight: '1.8',
    color: '#333',
  },
};
```

**Test it**: Go to `http://localhost:5173/save-actions`

---

## TASK 4: Create Demo Narrative (1 hour)

**File**: Create `frontend/src/pages/DemoNarrative.jsx`

**Copy from**: `PERSON_4_ACTIONS.md` - Search for "Step 4A: Create Demo Narrative Page"

Or use this shortened version (same logic, simpler):

```jsx
import React, { useState } from 'react';

const STEPS = [
  { title: '📊 Upload Customer Data', desc: 'Telecom uploads 1,000 customer records', link: '/upload' },
  { title: '🎯 Churn Analysis', desc: '150 high-risk customers identified in seconds', link: '/dashboard' },
  { title: '💰 ROI Calculation', desc: '$500K revenue at risk, $150K saveable', link: '/dashboard/roi' },
  { title: '🚀 Generate Messages', desc: 'Auto-personalized emails + SMS', link: '/save-actions' },
  { title: '🎨 Customer Widget', desc: 'Engagement tips on customer portal', link: '/demo' },
  { title: '📈 Impact', desc: '150 engaged customers, $150K protected', link: '#' },
];

export default function DemoNarrative() {
  const [step, setStep] = useState(0);
  const current = STEPS[step];
  
  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <div style={{...styles.progress, width: `${((step + 1) / STEPS.length) * 100}%`}}></div>
        
        <h1 style={styles.title}>{current.title}</h1>
        <p style={styles.description}>{current.desc}</p>
        
        <div style={styles.visual}>Demo Visualization</div>
        
        <div style={styles.actions}>
          <button onClick={() => setStep(Math.max(0, step - 1))} disabled={step === 0} style={styles.btn}>
            ← Previous
          </button>
          
          {current.link !== '#' && (
            <a href={current.link} style={{...styles.btn, background: '#667eea', color: 'white', textDecoration: 'none'}}>
              View Demo →
            </a>
          )}
          
          <button onClick={() => setStep(Math.min(STEPS.length - 1, step + 1))} disabled={step === STEPS.length - 1} style={styles.btn}>
            Next →
          </button>
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
    position: 'relative',
  },
  progress: {
    position: 'absolute',
    top: 0,
    left: 0,
    height: '4px',
    background: '#667eea',
    borderRadius: '20px 0 0 0',
    transition: 'width 0.3s',
  },
  title: {
    fontSize: '28px',
    marginBottom: '15px',
    marginTop: '10px',
  },
  description: {
    fontSize: '16px',
    color: '#666',
    marginBottom: '30px',
  },
  visual: {
    background: '#f5f5f5',
    padding: '60px',
    borderRadius: '12px',
    textAlign: 'center',
    color: '#667eea',
    fontWeight: 600,
    marginBottom: '30px',
  },
  actions: {
    display: 'flex',
    gap: '12px',
  },
  btn: {
    flex: 1,
    padding: '12px 24px',
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    background: '#f5f5f5',
    cursor: 'pointer',
    fontWeight: 600,
    fontSize: '14px',
    transition: 'all 0.3s',
  },
};
```

**Test it**: Go to `http://localhost:5173/demo-narrative`

---

## DONE! ✅

You've completed Person 4's main deliverables:
- ✅ Widget (already created)
- ✅ Demo Site
- ✅ Message Gallery  
- ✅ Demo Narrative

Now:
1. **Test everything** - Click through all pages
2. **Check for errors** - Open DevTools (F12)
3. **Test on mobile** - Drag browser window to narrow it
4. **Write presentation script** - Practice your demo
5. **Get backup screenshots** - Save images in case of demo issues

**You've got 19+ hours left. You're ahead of schedule!** 🎉

---

**Questions?** Ask backend/frontend team if endpoints aren't ready. Use mock data meanwhile!

Good luck! 🚀
