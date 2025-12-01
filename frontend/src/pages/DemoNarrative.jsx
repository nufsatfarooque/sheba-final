import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const narrativeSteps = [
  {
    number: 1,
    title: '📊 Upload Customer Data',
    subtitle: 'Step 1: Data Collection',
    description:
      'Start by uploading your customer dataset (CSV/Excel). The system accepts historical data including customer demographics, transaction history, service usage patterns, and any previous churn indicators.',
    details: [
      'Upload CSV/Excel files',
      'Map columns to customer fields',
      'Validate data quality',
      'Process 10K+ customer records in seconds',
    ],
    route: '/upload',
  },
  {
    number: 2,
    title: '🎯 Churn Analysis',
    subtitle: 'Step 2: ML Analysis',
    description:
      'The AI engine analyzes the data to identify at-risk customers. It calculates churn scores (0-100%) using machine learning models trained on historical churn patterns, engagement metrics, and behavioral indicators.',
    details: [
      'ML model processes data',
      'Churn scores calculated',
      'Risk segments identified',
      'Top 20% at-risk customers flagged',
    ],
    route: '/dashboard',
  },
  {
    number: 3,
    title: '💰 ROI & Impact',
    subtitle: 'Step 3: Business Impact',
    description:
      'See the financial potential. The system calculates customer lifetime value, potential revenue loss from churn, and shows you the ROI of the retention campaign. Visualize the impact across different customer segments.',
    details: [
      'Revenue impact analysis',
      'Customer lifetime value',
      'Retention potential: $150K',
      'ROI calculation: 300%',
    ],
    route: '/dashboard/roi',
  },
  {
    number: 4,
    title: '✉️ Generate Messages',
    subtitle: 'Step 4: AI-Powered Content',
    description:
      "SHEBA automatically generates personalized emails and SMS messages for each at-risk customer. Each message is tailored to their specific situation, preferences, and history with your company.",
    details: [
      'Personalized email templates',
      'SMS message generation',
      'A/B test variants',
      '3 messages auto-generated per customer',
    ],
    route: '/save-actions',
  },
  {
    number: 5,
    title: '🎁 Widget Embedding',
    subtitle: 'Step 5: Customer Engagement',
    description:
      'Embed the SHEBA widget on your customer portal. The widget displays personalized offers and engagement tips directly to customers, creating a seamless retention experience without leaving your platform.',
    details: [
      'Copy-paste widget code',
      'Works on any website',
      'Real-time personalization',
      'Mobile responsive design',
    ],
    route: '/demo',
  },
  {
    number: 6,
    title: '📈 Measure Impact',
    subtitle: 'Step 6: Results & Optimization',
    description:
      'Track the results in real-time. Monitor message open rates, click-through rates, customer responses, and most importantly: actual churn reduction. Use these insights to optimize future campaigns.',
    details: [
      'Email open rates',
      'SMS delivery confirmed',
      'Customer conversion tracking',
      'Churn reduction: 40-60%',
    ],
  },
]

export default function DemoNarrative() {
  const [currentStep, setCurrentStep] = useState(0)
  const navigate = useNavigate()
  const step = narrativeSteps[currentStep]

  const handleNext = () => {
    if (currentStep < narrativeSteps.length - 1) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleNavigateToStep = (route) => {
    if (route) {
      navigate(route)
    }
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8f9fa', padding: '40px 20px' }}>
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ marginBottom: '40px', textAlign: 'center' }}>
          <h1 style={{ margin: '0 0 10px 0', fontSize: '32px', color: '#1e293b', fontWeight: 'bold' }}>
            SHEBA Product Walkthrough
          </h1>
          <p style={{ margin: '0', color: '#64748b', fontSize: '16px' }}>
            See how AI-powered churn prediction and retention works in 6 simple steps
          </p>
        </div>

        {/* Progress Bar */}
        <div style={{ marginBottom: '40px' }}>
          <div
            style={{
              display: 'flex',
              gap: '10px',
              marginBottom: '15px',
            }}
          >
            {narrativeSteps.map((s, index) => (
              <div
                key={index}
                style={{
                  flex: 1,
                  height: '6px',
                  backgroundColor: index <= currentStep ? '#667eea' : '#e2e8f0',
                  borderRadius: '3px',
                  cursor: 'pointer',
                }}
                onClick={() => setCurrentStep(index)}
                title={s.title}
              />
            ))}
          </div>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              color: '#94a3b8',
              fontSize: '12px',
            }}
          >
            <div>Step {currentStep + 1}</div>
            <div>of {narrativeSteps.length}</div>
          </div>
        </div>

        {/* Main Content Card */}
        <div
          style={{
            backgroundColor: 'white',
            borderRadius: '12px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            overflow: 'hidden',
            marginBottom: '30px',
          }}
        >
          {/* Step Header */}
          <div
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              padding: '40px 30px',
              textAlign: 'center',
            }}
          >
            <div style={{ fontSize: '48px', marginBottom: '15px' }}>
              {step.title.split(' ')[0]}
            </div>
            <h2 style={{ margin: '0 0 8px 0', fontSize: '28px', fontWeight: 'bold' }}>
              {step.title.split(' ').slice(1).join(' ')}
            </h2>
            <p style={{ margin: '0', fontSize: '14px', opacity: 0.9 }}>
              {step.subtitle}
            </p>
          </div>

          {/* Step Content */}
          <div style={{ padding: '40px 30px' }}>
            <p
              style={{
                margin: '0 0 30px 0',
                fontSize: '16px',
                color: '#475569',
                lineHeight: '1.8',
              }}
            >
              {step.description}
            </p>

            {/* Details List */}
            <div style={{ marginBottom: '30px' }}>
              <h3
                style={{
                  margin: '0 0 15px 0',
                  fontSize: '14px',
                  color: '#64748b',
                  fontWeight: 'bold',
                  textTransform: 'uppercase',
                  letterSpacing: '0.5px',
                }}
              >
                Key Points:
              </h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px' }}>
                {step.details.map((detail, index) => (
                  <div
                    key={index}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: '10px',
                    }}
                  >
                    <div
                      style={{
                        width: '6px',
                        height: '6px',
                        backgroundColor: '#667eea',
                        borderRadius: '50%',
                        marginTop: '8px',
                        flexShrink: 0,
                      }}
                    />
                    <div style={{ fontSize: '14px', color: '#475569' }}>
                      {detail}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Visualization Placeholder */}
            <div
              style={{
                backgroundColor: '#f9fafb',
                border: '2px dashed #e2e8f0',
                borderRadius: '8px',
                padding: '40px',
                textAlign: 'center',
                marginBottom: '30px',
              }}
            >
              <div style={{ fontSize: '48px', marginBottom: '10px' }}>
                {step.number === 1 && '📁'}
                {step.number === 2 && '🤖'}
                {step.number === 3 && '💹'}
                {step.number === 4 && '✉️'}
                {step.number === 5 && '🎁'}
                {step.number === 6 && '📊'}
              </div>
              <p style={{ margin: '0', color: '#94a3b8', fontSize: '14px' }}>
                {step.number === 1 && 'Upload your customer data file'}
                {step.number === 2 && 'ML engine analyzes churn patterns'}
                {step.number === 3 && 'Financial impact dashboard'}
                {step.number === 4 && 'Personalized message generation'}
                {step.number === 5 && 'Customer-facing engagement widget'}
                {step.number === 6 && 'Real-time results tracking'}
              </p>
            </div>

            {/* CTA Button */}
            {step.route && (
              <button
                onClick={() => handleNavigateToStep(step.route)}
                style={{
                  width: '100%',
                  padding: '15px',
                  backgroundColor: '#667eea',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  fontSize: '16px',
                  marginBottom: '20px',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = '#5568d3'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = '#667eea'
                }}
              >
                View This Step in Action →
              </button>
            )}
          </div>
        </div>

        {/* Navigation */}
        <div
          style={{
            display: 'flex',
            gap: '15px',
            justifyContent: 'space-between',
            marginBottom: '30px',
          }}
        >
          <button
            onClick={handlePrevious}
            disabled={currentStep === 0}
            style={{
              flex: 1,
              padding: '12px',
              backgroundColor: currentStep === 0 ? '#f1f5f9' : '#e0e7ff',
              color: currentStep === 0 ? '#cbd5e1' : '#667eea',
              border: 'none',
              borderRadius: '8px',
              cursor: currentStep === 0 ? 'not-allowed' : 'pointer',
              fontWeight: 'bold',
              fontSize: '14px',
            }}
            onMouseEnter={(e) => {
              if (currentStep > 0) {
                e.currentTarget.style.backgroundColor = '#c7d2fe'
              }
            }}
            onMouseLeave={(e) => {
              if (currentStep > 0) {
                e.currentTarget.style.backgroundColor = '#e0e7ff'
              }
            }}
          >
            ← Previous
          </button>

          <button
            onClick={handleNext}
            disabled={currentStep === narrativeSteps.length - 1}
            style={{
              flex: 1,
              padding: '12px',
              backgroundColor: currentStep === narrativeSteps.length - 1 ? '#f1f5f9' : '#667eea',
              color: currentStep === narrativeSteps.length - 1 ? '#cbd5e1' : 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: currentStep === narrativeSteps.length - 1 ? 'not-allowed' : 'pointer',
              fontWeight: 'bold',
              fontSize: '14px',
            }}
            onMouseEnter={(e) => {
              if (currentStep < narrativeSteps.length - 1) {
                e.currentTarget.style.backgroundColor = '#5568d3'
              }
            }}
            onMouseLeave={(e) => {
              if (currentStep < narrativeSteps.length - 1) {
                e.currentTarget.style.backgroundColor = '#667eea'
              }
            }}
          >
            Next →
          </button>
        </div>

        {/* Quick Navigation */}
        <div
          style={{
            backgroundColor: 'white',
            borderRadius: '12px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            padding: '20px',
          }}
        >
          <h3
            style={{
              margin: '0 0 15px 0',
              fontSize: '14px',
              color: '#64748b',
              fontWeight: 'bold',
              textTransform: 'uppercase',
            }}
          >
            Jump to Step:
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
            {narrativeSteps.map((s, index) => (
              <button
                key={index}
                onClick={() => setCurrentStep(index)}
                style={{
                  padding: '12px',
                  backgroundColor: currentStep === index ? '#667eea' : '#f1f5f9',
                  color: currentStep === index ? 'white' : '#64748b',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  fontSize: '13px',
                  transition: 'all 0.2s ease',
                }}
                onMouseEnter={(e) => {
                  if (currentStep !== index) {
                    e.currentTarget.style.backgroundColor = '#e0e7ff'
                  }
                }}
                onMouseLeave={(e) => {
                  if (currentStep !== index) {
                    e.currentTarget.style.backgroundColor = '#f1f5f9'
                  }
                }}
              >
                {s.title.split(' ')[0]} Step {index + 1}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
