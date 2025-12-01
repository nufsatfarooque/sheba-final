import { useEffect, useState } from 'react'

export default function DemoSite() {
  const [widgetLoaded, setWidgetLoaded] = useState(false)
  const [activePage, setActivePage] = useState('dashboard')
  const [hoveredItem, setHoveredItem] = useState(null)

  useEffect(() => {
    // Try to load the widget script
    const loadWidget = () => {
      if (window.ShebaWidget) {
        try {
          window.ShebaWidget.init({
            org_api_key: 'demo-org-key',
            customer_id: 'cust-001',
            container_id: 'sheba-widget-container',
            api_url: 'http://localhost:8000',
          })
          setWidgetLoaded(true)
        } catch (err) {
          console.error('Widget init failed:', err)
          setWidgetLoaded(true)
        }
      } else {
        setWidgetLoaded(true)
      }
    }

    // Try loading widget after a short delay
    setTimeout(loadWidget, 500)
  }, [])

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8f9fa' }}>
      {/* Portal Header */}
      <div
        style={{
          backgroundColor: '#1e293b',
          color: 'white',
          padding: '20px 40px',
          borderBottom: '3px solid #667eea',
        }}
      >
        <h1 style={{ margin: 0, fontSize: '28px', fontWeight: 'bold' }}>
          Acme Telecom
        </h1>
        <p style={{ margin: '5px 0 0 0', color: '#cbd5e1' }}>
          Powered by Pulse
        </p>
      </div>

      <div style={{ display: 'flex', minHeight: 'calc(100vh - 100px)' }}>
        {/* Sidebar */}
        <div
          style={{
            width: '250px',
            backgroundColor: '#334155',
            color: 'white',
            padding: '30px 20px',
            borderRight: '1px solid #cbd5e1',
          }}
        >
          <div style={{ marginBottom: '30px' }}>
            <h3 style={{ margin: '0 0 15px 0', fontSize: '14px', color: '#cbd5e1' }}>
              ACCOUNT
            </h3>
            <div
              onClick={() => setActivePage('dashboard')}
              onMouseEnter={() => setHoveredItem('dashboard')}
              onMouseLeave={() => setHoveredItem(null)}
              style={{
                cursor: 'pointer',
                padding: '10px 12px',
                marginBottom: '8px',
                borderRadius: '6px',
                backgroundColor: activePage === 'dashboard' ? '#475569' : (hoveredItem === 'dashboard' ? '#3f4a57' : 'transparent'),
                color: activePage === 'dashboard' ? '#667eea' : 'white',
                fontWeight: activePage === 'dashboard' ? '600' : '400',
                transition: 'all 0.2s ease',
                borderLeft: activePage === 'dashboard' ? '3px solid #667eea' : '3px solid transparent',
                paddingLeft: activePage === 'dashboard' ? '9px' : '12px',
              }}
            >
              Dashboard
            </div>
            <div
              onClick={() => setActivePage('plans')}
              onMouseEnter={() => setHoveredItem('plans')}
              onMouseLeave={() => setHoveredItem(null)}
              style={{
                cursor: 'pointer',
                padding: '10px 12px',
                marginBottom: '8px',
                borderRadius: '6px',
                backgroundColor: activePage === 'plans' ? '#475569' : (hoveredItem === 'plans' ? '#3f4a57' : 'transparent'),
                color: activePage === 'plans' ? '#667eea' : 'white',
                fontWeight: activePage === 'plans' ? '600' : '400',
                transition: 'all 0.2s ease',
                borderLeft: activePage === 'plans' ? '3px solid #667eea' : '3px solid transparent',
                paddingLeft: activePage === 'plans' ? '9px' : '12px',
              }}
            >
              Plans & Pricing
            </div>
            <div
              onClick={() => setActivePage('billing')}
              onMouseEnter={() => setHoveredItem('billing')}
              onMouseLeave={() => setHoveredItem(null)}
              style={{
                cursor: 'pointer',
                padding: '10px 12px',
                marginBottom: '8px',
                borderRadius: '6px',
                backgroundColor: activePage === 'billing' ? '#475569' : (hoveredItem === 'billing' ? '#3f4a57' : 'transparent'),
                color: activePage === 'billing' ? '#667eea' : 'white',
                fontWeight: activePage === 'billing' ? '600' : '400',
                transition: 'all 0.2s ease',
                borderLeft: activePage === 'billing' ? '3px solid #667eea' : '3px solid transparent',
                paddingLeft: activePage === 'billing' ? '9px' : '12px',
              }}
            >
              Billing
            </div>
          </div>

          <div style={{ marginBottom: '30px' }}>
            <h3 style={{ margin: '0 0 15px 0', fontSize: '14px', color: '#cbd5e1' }}>
              SUPPORT
            </h3>
            <div
              onClick={() => setActivePage('help')}
              onMouseEnter={() => setHoveredItem('help')}
              onMouseLeave={() => setHoveredItem(null)}
              style={{
                cursor: 'pointer',
                padding: '10px 12px',
                marginBottom: '8px',
                borderRadius: '6px',
                backgroundColor: activePage === 'help' ? '#475569' : (hoveredItem === 'help' ? '#3f4a57' : 'transparent'),
                color: activePage === 'help' ? '#667eea' : 'white',
                fontWeight: activePage === 'help' ? '600' : '400',
                transition: 'all 0.2s ease',
                borderLeft: activePage === 'help' ? '3px solid #667eea' : '3px solid transparent',
                paddingLeft: activePage === 'help' ? '9px' : '12px',
              }}
            >
              Help Center
            </div>
            <div
              onClick={() => setActivePage('contact')}
              onMouseEnter={() => setHoveredItem('contact')}
              onMouseLeave={() => setHoveredItem(null)}
              style={{
                cursor: 'pointer',
                padding: '10px 12px',
                marginBottom: '8px',
                borderRadius: '6px',
                backgroundColor: activePage === 'contact' ? '#475569' : (hoveredItem === 'contact' ? '#3f4a57' : 'transparent'),
                color: activePage === 'contact' ? '#667eea' : 'white',
                fontWeight: activePage === 'contact' ? '600' : '400',
                transition: 'all 0.2s ease',
                borderLeft: activePage === 'contact' ? '3px solid #667eea' : '3px solid transparent',
                paddingLeft: activePage === 'contact' ? '9px' : '12px',
              }}
            >
              Contact Us
            </div>
          </div>

          <div
            style={{
              marginTop: '40px',
              padding: '15px',
              backgroundColor: '#475569',
              borderRadius: '8px',
              fontSize: '13px',
            }}
          >
            <p style={{ margin: 0, color: '#e2e8f0' }}>
              👤 Logged in as: <strong>John Doe</strong>
            </p>
          </div>
        </div>

        {/* Main Content */}
        <div style={{ flex: 1, padding: '40px' }}>
          {/* Welcome Section */}
          <div style={{ marginBottom: '40px' }}>
            <h2 style={{ margin: '0 0 10px 0', fontSize: '32px', color: '#1e293b' }}>
              {activePage === 'dashboard' && 'Welcome Back, John! 👋'}
              {activePage === 'plans' && 'Plans & Pricing 💳'}
              {activePage === 'billing' && 'Billing & Payments 💰'}
              {activePage === 'help' && 'Help Center ❓'}
              {activePage === 'contact' && 'Contact Us 📞'}
            </h2>
            <p style={{ margin: '0', color: '#64748b', fontSize: '16px' }}>
              {activePage === 'dashboard' && 'Here\'s your account summary for December 2024'}
              {activePage === 'plans' && 'Compare our plans and find the perfect fit for you'}
              {activePage === 'billing' && 'Manage your billing and payment methods'}
              {activePage === 'help' && 'Find answers to common questions'}
              {activePage === 'contact' && 'We\'re here to help - reach out anytime'}
            </p>
          </div>

          {/* Stats Cards - Show only on Dashboard */}
          {activePage === 'dashboard' && (
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '20px',
              marginBottom: '40px',
            }}
          >
            <div
              style={{
                backgroundColor: 'white',
                padding: '20px',
                borderRadius: '12px',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                borderLeft: '4px solid #667eea',
              }}
            >
              <div style={{ color: '#64748b', fontSize: '13px', marginBottom: '8px' }}>
                Current Plan
              </div>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1e293b' }}>
                Premium
              </div>
              <div style={{ color: '#94a3b8', fontSize: '12px', marginTop: '8px' }}>
                $99/month
              </div>
            </div>

            <div
              style={{
                backgroundColor: 'white',
                padding: '20px',
                borderRadius: '12px',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                borderLeft: '4px solid #10b981',
              }}
            >
              <div style={{ color: '#64748b', fontSize: '13px', marginBottom: '8px' }}>
                Data Used
              </div>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1e293b' }}>
                45 GB
              </div>
              <div style={{ color: '#94a3b8', fontSize: '12px', marginTop: '8px' }}>
                of 100 GB available
              </div>
            </div>

            <div
              style={{
                backgroundColor: 'white',
                padding: '20px',
                borderRadius: '12px',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                borderLeft: '4px solid #f59e0b',
              }}
            >
              <div style={{ color: '#64748b', fontSize: '13px', marginBottom: '8px' }}>
                Last Payment
              </div>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1e293b' }}>
                Nov 28
              </div>
              <div style={{ color: '#94a3b8', fontSize: '12px', marginTop: '8px' }}>
                Next: Dec 28
              </div>
            </div>
          </div>
          )}

          {/* Content by page */}
          {activePage === 'dashboard' && (
          <>
          {/* SHEBA Widget Section */}
          <div
            style={{
              backgroundColor: 'white',
              padding: '30px',
              borderRadius: '12px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
              marginBottom: '40px',
            }}
          >
            <h3
              style={{
                margin: '0 0 10px 0',
                fontSize: '18px',
                color: '#1e293b',
                fontWeight: 'bold',
              }}
            >
              💡 Personalized Offer from Pulse
            </h3>
            <p style={{ margin: '0 0 20px 0', color: '#64748b', fontSize: '14px' }}>
              Pulse AI has analyzed your account and prepared a personalized offer just for you:
            </p>

            {/* Widget Container */}
            <div
              id="sheba-widget-container"
              style={{
                minHeight: '300px',
                backgroundColor: '#f9fafb',
                borderRadius: '8px',
                display: 'block',
                border: '2px dashed #e2e8f0',
                marginTop: '15px',
                padding: '20px',
              }}
            >
              {!widgetLoaded && (
                <div style={{ textAlign: 'center', color: '#94a3b8', padding: '60px 20px' }}>
                  <div style={{ fontSize: '48px', marginBottom: '15px' }}>🎁</div>
                  <div style={{ fontSize: '16px', marginBottom: '10px', fontWeight: 'bold' }}>
                    Pulse Widget - Customer Engagement
                  </div>
                  <div style={{ fontSize: '14px', marginBottom: '20px', color: '#64748b' }}>
                    Here's where the Pulse widget appears with AI-powered personalization:
                  </div>
                  <ul style={{ fontSize: '13px', color: '#64748b', textAlign: 'left', display: 'inline-block' }}>
                    <li>🎯 Your churn risk score & engagement level</li>
                    <li>💝 AI-personalized retention offer</li>
                    <li>✨ One-click action to claim the offer</li>
                    <li>📊 Tips to maximize your account value</li>
                  </ul>
                  <div style={{ marginTop: '20px', fontSize: '12px', color: '#94a3b8' }}>
                    Powered by Pulse Identity Intelligence Platform
                  </div>
                </div>
              )}
            </div>
          </div>
          </>
          )}

          {activePage === 'plans' && (
          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
              <div style={{ border: '1px solid #e2e8f0', padding: '25px', borderRadius: '8px', textAlign: 'center' }}>
                <div style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '10px', color: '#1e293b' }}>Starter</div>
                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#667eea', marginBottom: '15px' }}>$29<span style={{ fontSize: '16px', color: '#64748b' }}>/mo</span></div>
                <ul style={{ textAlign: 'left', fontSize: '14px', color: '#64748b', marginBottom: '20px', listStyle: 'none', padding: 0 }}>
                  <li>✓ 50 GB Storage</li>
                  <li>✓ Email Support</li>
                  <li>✓ Basic Analytics</li>
                </ul>
                <button style={{ width: '100%', padding: '10px', backgroundColor: '#667eea', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}>Choose Plan</button>
              </div>
              <div style={{ border: '2px solid #667eea', padding: '25px', borderRadius: '8px', textAlign: 'center', backgroundColor: '#f0f4ff' }}>
                <div style={{ fontSize: '12px', color: '#667eea', fontWeight: 'bold', marginBottom: '10px' }}>POPULAR</div>
                <div style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '10px', color: '#1e293b' }}>Premium</div>
                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#667eea', marginBottom: '15px' }}>$99<span style={{ fontSize: '16px', color: '#64748b' }}>/mo</span></div>
                <ul style={{ textAlign: 'left', fontSize: '14px', color: '#64748b', marginBottom: '20px', listStyle: 'none', padding: 0 }}>
                  <li>✓ 100 GB Storage</li>
                  <li>✓ Priority Support</li>
                  <li>✓ Advanced Analytics</li>
                </ul>
                <button style={{ width: '100%', padding: '10px', backgroundColor: '#667eea', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}>Current Plan</button>
              </div>
              <div style={{ border: '1px solid #e2e8f0', padding: '25px', borderRadius: '8px', textAlign: 'center' }}>
                <div style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '10px', color: '#1e293b' }}>Enterprise</div>
                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#667eea', marginBottom: '15px' }}>Custom</div>
                <ul style={{ textAlign: 'left', fontSize: '14px', color: '#64748b', marginBottom: '20px', listStyle: 'none', padding: 0 }}>
                  <li>✓ Unlimited Storage</li>
                  <li>✓ 24/7 Support</li>
                  <li>✓ Custom Features</li>
                </ul>
                <button style={{ width: '100%', padding: '10px', backgroundColor: '#e2e8f0', color: '#1e293b', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}>Contact Sales</button>
              </div>
            </div>
          </div>
          )}

          {activePage === 'billing' && (
          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <div style={{ marginBottom: '30px' }}>
              <h3 style={{ color: '#1e293b', marginBottom: '15px' }}>Payment Methods</h3>
              <div style={{ border: '1px solid #e2e8f0', padding: '15px', borderRadius: '8px', marginBottom: '10px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>💳 Visa ending in 4242</div>
                  <button style={{ padding: '5px 10px', backgroundColor: '#667eea', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '12px' }}>Default</button>
                </div>
              </div>
              <button style={{ padding: '10px 15px', border: '1px solid #667eea', color: '#667eea', backgroundColor: 'white', borderRadius: '6px', cursor: 'pointer', fontWeight: '500' }}>+ Add Payment Method</button>
            </div>
            <div style={{ borderTop: '1px solid #e2e8f0', paddingTop: '30px' }}>
              <h3 style={{ color: '#1e293b', marginBottom: '15px' }}>Billing History</h3>
              <div style={{ border: '1px solid #e2e8f0', borderRadius: '8px', overflow: 'hidden' }}>
                <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr auto auto', padding: '15px', backgroundColor: '#f8f9fa', fontWeight: 'bold', fontSize: '14px' }}>
                  <div>Date</div><div>Description</div><div>Amount</div><div>Status</div>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr auto auto', padding: '15px', borderTop: '1px solid #e2e8f0', fontSize: '14px' }}>
                  <div>Nov 28</div><div>Premium Plan</div><div>$99.00</div><div style={{ color: '#10b981', fontWeight: 'bold' }}>Paid</div>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr auto auto', padding: '15px', borderTop: '1px solid #e2e8f0', fontSize: '14px' }}>
                  <div>Oct 28</div><div>Premium Plan</div><div>$99.00</div><div style={{ color: '#10b981', fontWeight: 'bold' }}>Paid</div>
                </div>
              </div>
            </div>
          </div>
          )}

          {activePage === 'help' && (
          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <div style={{ display: 'grid', gap: '20px' }}>
              <div style={{ border: '1px solid #e2e8f0', padding: '20px', borderRadius: '8px', cursor: 'pointer' }}>
                <div style={{ fontWeight: 'bold', color: '#1e293b', marginBottom: '8px' }}>How do I upgrade my plan?</div>
                <div style={{ color: '#64748b', fontSize: '14px' }}>Go to Plans & Pricing to see all available options and click Choose Plan.</div>
              </div>
              <div style={{ border: '1px solid #e2e8f0', padding: '20px', borderRadius: '8px', cursor: 'pointer' }}>
                <div style={{ fontWeight: 'bold', color: '#1e293b', marginBottom: '8px' }}>Can I cancel anytime?</div>
                <div style={{ color: '#64748b', fontSize: '14px' }}>Yes, you can cancel your plan anytime without penalties. Your access continues until the end of billing cycle.</div>
              </div>
              <div style={{ border: '1px solid #e2e8f0', padding: '20px', borderRadius: '8px', cursor: 'pointer' }}>
                <div style={{ fontWeight: 'bold', color: '#1e293b', marginBottom: '8px' }}>What payment methods do you accept?</div>
                <div style={{ color: '#64748b', fontSize: '14px' }}>We accept all major credit cards and PayPal. Invoicing available for enterprise plans.</div>
              </div>
              <div style={{ border: '1px solid #e2e8f0', padding: '20px', borderRadius: '8px', cursor: 'pointer' }}>
                <div style={{ fontWeight: 'bold', color: '#1e293b', marginBottom: '8px' }}>How secure is my data?</div>
                <div style={{ color: '#64748b', fontSize: '14px' }}>We use enterprise-grade encryption and comply with SOC 2, GDPR, and HIPAA standards.</div>
              </div>
            </div>
          </div>
          )}

          {activePage === 'contact' && (
          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '30px' }}>
              <div>
                <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#1e293b', marginBottom: '10px' }}>📧 Email</div>
                <div style={{ color: '#64748b' }}>support@acme-telecom.com</div>
                <div style={{ color: '#64748b', fontSize: '13px', marginTop: '5px' }}>Response time: 2 hours</div>
              </div>
              <div>
                <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#1e293b', marginBottom: '10px' }}>📞 Phone</div>
                <div style={{ color: '#64748b' }}>1-800-ACME-TEL</div>
                <div style={{ color: '#64748b', fontSize: '13px', marginTop: '5px' }}>Mon-Fri 9am-6pm EST</div>
              </div>
              <div>
                <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#1e293b', marginBottom: '10px' }}>💬 Chat</div>
                <div style={{ color: '#64748b' }}>Live chat available</div>
                <div style={{ color: '#64748b', fontSize: '13px', marginTop: '5px' }}>24/7 support</div>
              </div>
            </div>
          </div>
          )}

          {/* Recent Activity - Show only on Dashboard */}
          {activePage === 'dashboard' && (
          <div
            style={{
              backgroundColor: 'white',
              padding: '30px',
              borderRadius: '12px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            }}
          >
            <h3
              style={{
                margin: '0 0 20px 0',
                fontSize: '18px',
                color: '#1e293b',
                fontWeight: 'bold',
              }}
            >
              Recent Activity
            </h3>

            <div style={{ borderTop: '1px solid #e2e8f0', paddingTop: '15px' }}>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  paddingBottom: '15px',
                  borderBottom: '1px solid #e2e8f0',
                }}
              >
                <div>
                  <div style={{ fontWeight: 'bold', color: '#1e293b' }}>
                    Premium Plan Renewed
                  </div>
                  <div style={{ fontSize: '13px', color: '#94a3b8' }}>Nov 28, 2024</div>
                </div>
                <div style={{ color: '#10b981', fontWeight: 'bold' }}>$99.00</div>
              </div>

              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  paddingBottom: '15px',
                  borderBottom: '1px solid #e2e8f0',
                  paddingTop: '15px',
                }}
              >
                <div>
                  <div style={{ fontWeight: 'bold', color: '#1e293b' }}>
                    Data Overage Charge
                  </div>
                  <div style={{ fontSize: '13px', color: '#94a3b8' }}>Nov 15, 2024</div>
                </div>
                <div style={{ color: '#ef4444', fontWeight: 'bold' }}>$15.50</div>
              </div>

              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  paddingTop: '15px',
                }}
              >
                <div>
                  <div style={{ fontWeight: 'bold', color: '#1e293b' }}>
                    Plan Upgraded
                  </div>
                  <div style={{ fontSize: '13px', color: '#94a3b8' }}>Nov 1, 2024</div>
                </div>
                <div style={{ color: '#10b981', fontWeight: 'bold' }}>Activated</div>
              </div>
            </div>
          </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div
        style={{
          backgroundColor: '#1e293b',
          color: '#cbd5e1',
          padding: '20px 40px',
          textAlign: 'center',
          borderTop: '1px solid #334155',
        }}
      >
        <p style={{ margin: 0, fontSize: '13px' }}>
          © 2024 Acme Telecom. All rights reserved. | Powered by Pulse
        </p>
      </div>
    </div>
  )
}
