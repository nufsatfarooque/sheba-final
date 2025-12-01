import { useState } from 'react'

const mockSaveActions = [
  {
    id: 1,
    company: 'TechCorp Inc.',
    customerId: 'TC-001',
    riskScore: 0.92,
    action: 'Premium Retention Offer',
    email: {
      subject: 'Exclusive: 30% Off Premium Plus - Just For You!',
      body: `Hi Alex,

We noticed you've been exploring other providers. We don't want to see you go!

As a valued TechCorp customer, we're offering you something special:

🎁 30% OFF our Premium Plus plan for 12 months
💰 Save $360 annually
⭐ Free priority support upgrade
🚀 Unlimited data access

This offer expires in 48 hours.

Claim Your Offer: https://checkout.techcorp.io/offers/premium-plus-30off

Questions? Reply to this email or call us at 1-800-TECH-911.

Best regards,
The TechCorp Team`,
    },
    sms: 'TechCorp: Exclusive 30% off Premium Plus just for you! 48hrs only. Claim: https://t.co/offer123',
    revenue: 360,
    churnRisk: 'High',
  },
  {
    id: 2,
    company: 'RetailGo Corp',
    customerId: 'RG-042',
    riskScore: 0.85,
    action: 'Loyalty Bonus',
    email: {
      subject: 'Your Loyalty Reward: Free Month of Service',
      body: `Hello Sarah,

We appreciate your 3 years of loyalty! As a token of our appreciation:

🎉 Free 1 Month of Premium Service
📱 Upgrade your phone for just $99
🎁 Extra 50GB bonus data

Your loyalty means everything to us. Let's celebrate together!

Activate Your Reward: https://loyalty.retailgo.io/claim/sarah-p

Questions? We're here to help at support@retailgo.io

Thank you for being awesome!
RetailGo Team`,
    },
    sms: 'RetailGo: Congrats! You have earned a free month. Claim your reward: https://t.co/reward456',
    revenue: 99,
    churnRisk: 'Medium',
  },
  {
    id: 3,
    company: 'FinanceFlow',
    customerId: 'FF-087',
    riskScore: 0.78,
    action: 'Service Improvement',
    email: {
      subject: 'We Listened: New Features You Requested',
      body: `Hi Jordan,

Your feedback helped us build something amazing!

You asked for it, we built it:

✨ New AI-powered expense tracking
📊 Real-time financial dashboard
🔒 Enhanced security features
⚡ 50% faster transactions

Upgrade now and get 3 months free: https://app.financeflow.io/new-features

We're excited to show you what's new!

The FinanceFlow Team`,
    },
    sms: 'FinanceFlow: New AI features just launched! Try now with 3 months free: https://t.co/features789',
    revenue: 150,
    churnRisk: 'Low',
  },
]

export default function SaveActionGallery() {
  const [selectedAction, setSelectedAction] = useState(null)
  const [previewType, setPreviewType] = useState('email')

  const totalRevenue = mockSaveActions.reduce((sum, action) => sum + action.revenue, 0)
  const highRiskCount = mockSaveActions.filter((a) => a.churnRisk === 'High').length
  const mediumRiskCount = mockSaveActions.filter((a) => a.churnRisk === 'Medium').length

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8f9fa', padding: '40px 20px' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ marginBottom: '40px' }}>
          <h1 style={{ margin: '0 0 10px 0', fontSize: '32px', color: '#1e293b', fontWeight: 'bold' }}>
            Pulse AI-Generated Save Actions
          </h1>
          <p style={{ margin: '0', color: '#64748b', fontSize: '16px' }}>
            AI-personalized retention messages for at-risk customers
          </p>
        </div>

        {/* Stats */}
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
              Total Revenue Impact
            </div>
            <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#1e293b' }}>
              ${totalRevenue}
            </div>
            <div style={{ color: '#94a3b8', fontSize: '12px', marginTop: '8px' }}>
              Potential savings from retention
            </div>
          </div>

          <div
            style={{
              backgroundColor: 'white',
              padding: '20px',
              borderRadius: '12px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
              borderLeft: '4px solid #ef4444',
            }}
          >
            <div style={{ color: '#64748b', fontSize: '13px', marginBottom: '8px' }}>
              High Risk Customers
            </div>
            <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#1e293b' }}>
              {highRiskCount}
            </div>
            <div style={{ color: '#94a3b8', fontSize: '12px', marginTop: '8px' }}>
              Need immediate attention
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
              Messages Ready
            </div>
            <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#1e293b' }}>
              {mockSaveActions.length}
            </div>
            <div style={{ color: '#94a3b8', fontSize: '12px', marginTop: '8px' }}>
              Auto-generated & ready to send
            </div>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px' }}>
          {/* Gallery */}
          <div>
            <h2 style={{ margin: '0 0 20px 0', fontSize: '20px', color: '#1e293b', fontWeight: 'bold' }}>
              Customer Messages
            </h2>

            <div style={{ display: 'grid', gap: '15px' }}>
              {mockSaveActions.map((action) => (
                <div
                  key={action.id}
                  onClick={() => {
                    setSelectedAction(action)
                    setPreviewType('email')
                  }}
                  style={{
                    backgroundColor: 'white',
                    padding: '20px',
                    borderRadius: '12px',
                    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                    cursor: 'pointer',
                    border: selectedAction?.id === action.id ? '2px solid #667eea' : '2px solid transparent',
                    transition: 'all 0.3s ease',
                  }}
                  onMouseEnter={(e) => {
                    if (selectedAction?.id !== action.id) {
                      e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)'
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (selectedAction?.id !== action.id) {
                      e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)'
                    }
                  }}
                >
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'start',
                      marginBottom: '10px',
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: 'bold', color: '#1e293b', fontSize: '15px' }}>
                        {action.company}
                      </div>
                      <div style={{ fontSize: '13px', color: '#94a3b8', marginTop: '4px' }}>
                        {action.customerId}
                      </div>
                    </div>
                    <div
                      style={{
                        backgroundColor: action.churnRisk === 'High' ? '#fee2e2' : action.churnRisk === 'Medium' ? '#fef3c7' : '#dcfce7',
                        color: action.churnRisk === 'High' ? '#991b1b' : action.churnRisk === 'Medium' ? '#92400e' : '#166534',
                        padding: '4px 12px',
                        borderRadius: '20px',
                        fontSize: '12px',
                        fontWeight: 'bold',
                      }}
                    >
                      {action.churnRisk} Risk
                    </div>
                  </div>

                  <div
                    style={{
                      fontSize: '14px',
                      color: '#64748b',
                      marginBottom: '10px',
                    }}
                  >
                    {action.action}
                  </div>

                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                    }}
                  >
                    <div
                      style={{
                        fontSize: '12px',
                        color: '#94a3b8',
                      }}
                    >
                      Churn Score: {(action.riskScore * 100).toFixed(0)}%
                    </div>
                    <div
                      style={{
                        fontSize: '14px',
                        fontWeight: 'bold',
                        color: '#10b981',
                      }}
                    >
                      +${action.revenue}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Preview */}
          <div>
            <h2 style={{ margin: '0 0 20px 0', fontSize: '20px', color: '#1e293b', fontWeight: 'bold' }}>
              Message Preview
            </h2>

            {selectedAction ? (
              <div
                style={{
                  backgroundColor: 'white',
                  borderRadius: '12px',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                  overflow: 'hidden',
                }}
              >
                {/* Preview Tabs */}
                <div
                  style={{
                    display: 'flex',
                    borderBottom: '1px solid #e2e8f0',
                    backgroundColor: '#f9fafb',
                  }}
                >
                  <button
                    onClick={() => setPreviewType('email')}
                    style={{
                      flex: 1,
                      padding: '15px',
                      border: 'none',
                      backgroundColor: previewType === 'email' ? 'white' : 'transparent',
                      borderBottom: previewType === 'email' ? '2px solid #667eea' : 'none',
                      cursor: 'pointer',
                      fontWeight: previewType === 'email' ? 'bold' : 'normal',
                      color: previewType === 'email' ? '#667eea' : '#64748b',
                      fontSize: '14px',
                    }}
                  >
                    📧 Email
                  </button>
                  <button
                    onClick={() => setPreviewType('sms')}
                    style={{
                      flex: 1,
                      padding: '15px',
                      border: 'none',
                      backgroundColor: previewType === 'sms' ? 'white' : 'transparent',
                      borderBottom: previewType === 'sms' ? '2px solid #667eea' : 'none',
                      cursor: 'pointer',
                      fontWeight: previewType === 'sms' ? 'bold' : 'normal',
                      color: previewType === 'sms' ? '#667eea' : '#64748b',
                      fontSize: '14px',
                    }}
                  >
                    📱 SMS
                  </button>
                </div>

                {/* Preview Content */}
                <div style={{ padding: '20px' }}>
                  {previewType === 'email' ? (
                    <div>
                      <div style={{ marginBottom: '15px' }}>
                        <div style={{ fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>
                          To:
                        </div>
                        <div style={{ fontSize: '14px', fontWeight: 'bold', color: '#1e293b' }}>
                          {selectedAction.company}
                        </div>
                      </div>

                      <div style={{ marginBottom: '20px' }}>
                        <div style={{ fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>
                          Subject:
                        </div>
                        <div style={{ fontSize: '14px', fontWeight: 'bold', color: '#667eea' }}>
                          {selectedAction.email.subject}
                        </div>
                      </div>

                      <div
                        style={{
                          backgroundColor: '#f9fafb',
                          padding: '15px',
                          borderRadius: '8px',
                          fontSize: '13px',
                          color: '#475569',
                          lineHeight: '1.6',
                          whiteSpace: 'pre-wrap',
                          wordWrap: 'break-word',
                          maxHeight: '400px',
                          overflowY: 'auto',
                        }}
                      >
                        {selectedAction.email.body}
                      </div>
                    </div>
                  ) : (
                    <div>
                      <div style={{ marginBottom: '15px' }}>
                        <div style={{ fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>
                          Message:
                        </div>
                      </div>

                      <div
                        style={{
                          backgroundColor: '#e0e7ff',
                          padding: '15px',
                          borderRadius: '8px',
                          fontSize: '14px',
                          color: '#3730a3',
                          lineHeight: '1.6',
                          whiteSpace: 'pre-wrap',
                          wordWrap: 'break-word',
                        }}
                      >
                        {selectedAction.sms}
                      </div>

                      <div
                        style={{
                          marginTop: '15px',
                          padding: '10px',
                          backgroundColor: '#f0fdf4',
                          borderRadius: '8px',
                          fontSize: '12px',
                          color: '#166534',
                        }}
                      >
                        Character count: {selectedAction.sms.length}
                      </div>
                    </div>
                  )}

                  {/* Action Buttons */}
                  <div
                    style={{
                      display: 'flex',
                      gap: '10px',
                      marginTop: '20px',
                      paddingTop: '20px',
                      borderTop: '1px solid #e2e8f0',
                    }}
                  >
                    <button
                      style={{
                        flex: 1,
                        padding: '10px 15px',
                        backgroundColor: '#667eea',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        fontWeight: 'bold',
                        fontSize: '14px',
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.backgroundColor = '#5568d3'
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.backgroundColor = '#667eea'
                      }}
                    >
                      {previewType === 'email' ? 'Send Email' : 'Send SMS'}
                    </button>
                    <button
                      style={{
                        flex: 1,
                        padding: '10px 15px',
                        backgroundColor: '#f1f5f9',
                        color: '#64748b',
                        border: '1px solid #e2e8f0',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        fontWeight: 'bold',
                        fontSize: '14px',
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.backgroundColor = '#e2e8f0'
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.backgroundColor = '#f1f5f9'
                      }}
                    >
                      Edit
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div
                style={{
                  backgroundColor: 'white',
                  padding: '40px 20px',
                  borderRadius: '12px',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                  textAlign: 'center',
                  color: '#94a3b8',
                }}
              >
                <div style={{ fontSize: '40px', marginBottom: '10px' }}>👈</div>
                <div>Select a message to preview</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
