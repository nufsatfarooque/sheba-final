import { useEffect, useState } from 'react'

export default function DemoSite() {
  const [widgetLoaded, setWidgetLoaded] = useState(false)

  useEffect(() => {
    // Load the widget script
    if (!window.ShebaWidget) {
      const script = document.createElement('script')
      script.src = '/sheba-widget.js'
      script.onload = () => {
        // Initialize the widget
        setTimeout(() => {
          if (window.ShebaWidget) {
            window.ShebaWidget.init({
              org_api_key: 'demo-org-key',
              customer_id: 'cust-001',
              container_id: 'sheba-widget-container',
              api_url: 'http://localhost:8000',
            })
            setWidgetLoaded(true)
          }
        }, 100)
      }
      script.onerror = () => {
        console.error('Failed to load widget script')
        setWidgetLoaded(true) // Still show demo even if widget fails
      }
      document.body.appendChild(script)
    } else {
      window.ShebaWidget.init({
        org_api_key: 'demo-org-key',
        customer_id: 'cust-001',
        container_id: 'sheba-widget-container',
        api_url: 'http://localhost:8000',
      })
      setWidgetLoaded(true)
    }
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
          Customer Portal
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
            <div style={{ cursor: 'pointer', padding: '10px', marginBottom: '8px' }}>
              Dashboard
            </div>
            <div style={{ cursor: 'pointer', padding: '10px', marginBottom: '8px' }}>
              Plans & Pricing
            </div>
            <div style={{ cursor: 'pointer', padding: '10px', marginBottom: '8px' }}>
              Billing
            </div>
          </div>

          <div style={{ marginBottom: '30px' }}>
            <h3 style={{ margin: '0 0 15px 0', fontSize: '14px', color: '#cbd5e1' }}>
              SUPPORT
            </h3>
            <div style={{ cursor: 'pointer', padding: '10px', marginBottom: '8px' }}>
              Help Center
            </div>
            <div style={{ cursor: 'pointer', padding: '10px', marginBottom: '8px' }}>
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
              Welcome Back, John! 👋
            </h2>
            <p style={{ margin: '0', color: '#64748b', fontSize: '16px' }}>
              Here's your account summary for December 2024
            </p>
          </div>

          {/* Stats Cards */}
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
              💡 Special Offer Just For You
            </h3>
            <p style={{ margin: '0 0 20px 0', color: '#64748b', fontSize: '14px' }}>
              We've prepared something special based on your account usage. Click below to learn more:
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
                    SHEBA Widget Demo
                  </div>
                  <div style={{ fontSize: '14px', marginBottom: '20px', color: '#64748b' }}>
                    Here's where the personalized widget would appear with:
                  </div>
                  <ul style={{ fontSize: '13px', color: '#64748b', textAlign: 'left', display: 'inline-block' }}>
                    <li>Your loyalty score & engagement level</li>
                    <li>Personalized retention offer</li>
                    <li>Action button to claim the offer</li>
                    <li>Tips to maximize your plan</li>
                  </ul>
                  <div style={{ marginTop: '20px', fontSize: '12px', color: '#94a3b8' }}>
                    Widget is loading from: /sheba-widget.js
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Recent Activity */}
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
          © 2024 Acme Telecom. All rights reserved. | Powered by SHEBA
        </p>
      </div>
    </div>
  )
}
