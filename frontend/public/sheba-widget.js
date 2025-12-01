/**
 * Sheba Customer Engagement Widget
 * Version: 1.0.0
 * 
 * Embeddable widget for customer portals
 * Shows: Loyalty score, engagement tips, personalized offers
 * 
 * Usage:
 * <script src="https://your-api.com/sheba-widget.js"></script>
 * <div id="sheba-widget"></div>
 * <script>
 *   ShebaWidget.init({
 *     org_api_key: 'pk_live_xyz',
 *     customer_id: 'cust_123',
 *     container_id: 'sheba-widget'
 *   });
 * </script>
 */

(function() {
  'use strict';

  // CSS Styles (injected into page)
  const WIDGET_CSS = `
    .sheba-widget-container {
      all: initial;
      display: block;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    .sheba-widget {
      box-sizing: border-box;
      max-width: 100%;
      width: 100%;
      margin: 0;
      padding: 24px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 12px;
      color: white;
      box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
      overflow: hidden;
    }

    .sheba-widget * {
      box-sizing: border-box;
    }

    .sheba-widget-header {
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .sheba-widget-logo {
      font-size: 24px;
      font-weight: bold;
    }

    .sheba-widget-title {
      margin: 0;
      font-size: 20px;
      font-weight: 600;
      line-height: 1.2;
    }

    .sheba-widget-subtitle {
      margin: 4px 0 0 0;
      font-size: 13px;
      opacity: 0.9;
    }

    .sheba-widget-stats {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 20px;
      background: rgba(255, 255, 255, 0.1);
      padding: 16px;
      border-radius: 8px;
    }

    .sheba-widget-stat {
      text-align: center;
    }

    .sheba-widget-stat-value {
      font-size: 32px;
      font-weight: 700;
      line-height: 1;
      margin-bottom: 4px;
    }

    .sheba-widget-stat-label {
      font-size: 12px;
      opacity: 0.85;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .sheba-widget-section {
      margin-bottom: 16px;
    }

    .sheba-widget-section-label {
      font-size: 12px;
      opacity: 0.8;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 8px;
      font-weight: 600;
    }

    .sheba-widget-section-content {
      background: rgba(255, 255, 255, 0.15);
      padding: 12px;
      border-radius: 6px;
      font-size: 14px;
      line-height: 1.5;
    }

    .sheba-widget-tips {
      list-style: none;
      margin: 0;
      padding: 0;
    }

    .sheba-widget-tip {
      padding: 8px 0;
      font-size: 13px;
      line-height: 1.4;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .sheba-widget-tip:last-child {
      border-bottom: none;
    }

    .sheba-widget-tip::before {
      content: '💡 ';
      margin-right: 6px;
    }

    .sheba-widget-offer {
      background: rgba(255, 255, 255, 0.2);
      padding: 12px;
      border-radius: 6px;
      margin: 12px 0;
      font-size: 13px;
      font-weight: 500;
    }

    .sheba-widget-button {
      display: inline-block;
      margin-top: 16px;
      padding: 12px 24px;
      background: white;
      color: #667eea;
      border: none;
      border-radius: 6px;
      font-weight: 600;
      font-size: 14px;
      cursor: pointer;
      transition: all 0.2s ease;
      text-decoration: none;
      text-align: center;
      width: 100%;
    }

    .sheba-widget-button:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(255, 255, 255, 0.3);
    }

    .sheba-widget-button:active {
      transform: translateY(0);
    }

    .sheba-widget-loading {
      text-align: center;
      padding: 32px 24px;
      font-size: 14px;
      opacity: 0.9;
    }

    .sheba-widget-spinner {
      display: inline-block;
      width: 20px;
      height: 20px;
      border: 3px solid rgba(255, 255, 255, 0.3);
      border-top-color: white;
      border-radius: 50%;
      animation: sheba-spin 0.8s linear infinite;
      margin-right: 8px;
      vertical-align: middle;
    }

    @keyframes sheba-spin {
      to { transform: rotate(360deg); }
    }

    .sheba-widget-error {
      background: rgba(239, 68, 68, 0.2);
      border: 1px solid rgba(239, 68, 68, 0.4);
      padding: 12px;
      border-radius: 6px;
      font-size: 13px;
      line-height: 1.4;
    }

    .sheba-widget-badge {
      display: inline-block;
      padding: 4px 12px;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      white-space: nowrap;
    }

    /* Responsive */
    @media (max-width: 480px) {
      .sheba-widget {
        padding: 16px;
      }

      .sheba-widget-stats {
        grid-template-columns: 1fr;
      }

      .sheba-widget-stat-value {
        font-size: 28px;
      }

      .sheba-widget-title {
        font-size: 18px;
      }
    }
  `;

  // Global Widget Object
  window.ShebaWidget = {
    version: '1.0.0',
    
    /**
     * Initialize widget
     * @param {Object} config - Configuration object
     * @param {string} config.org_api_key - Organization API key (required)
     * @param {string} config.customer_id - Customer ID (required)
     * @param {string} config.container_id - Container element ID (default: 'sheba-widget')
     * @param {string} config.api_url - Backend API URL (default: http://localhost:8000)
     */
    init: async function(config) {
      try {
        // Validate config
        if (!config || typeof config !== 'object') {
          console.error('[ShebaWidget] Config must be an object');
          return;
        }

        if (!config.org_api_key || !config.customer_id) {
          console.error('[ShebaWidget] Missing required config: org_api_key, customer_id');
          return;
        }

        const container = document.getElementById(config.container_id || 'sheba-widget');
        if (!container) {
          console.error('[ShebaWidget] Container element not found');
          return;
        }

        // Inject CSS once
        if (!document.getElementById('sheba-widget-styles')) {
          const style = document.createElement('style');
          style.id = 'sheba-widget-styles';
          style.textContent = WIDGET_CSS;
          document.head.appendChild(style);
        }

        // Show loading state
        container.innerHTML = `
          <div class="sheba-widget-container">
            <div class="sheba-widget">
              <div class="sheba-widget-loading">
                <span class="sheba-widget-spinner"></span> Loading...
              </div>
            </div>
          </div>
        `;

        // Fetch widget data
        const apiUrl = config.api_url || 'http://localhost:8000';
        const endpoint = `${apiUrl}/api/v1/widget/customer_view`;
        const params = new URLSearchParams({
          api_key: config.org_api_key,
          customer_id: config.customer_id
        });

        const response = await fetch(`${endpoint}?${params}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          // Add CORS headers if needed
          mode: 'cors',
          credentials: 'omit'
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        // Validate response
        if (!data.customer_name) {
          throw new Error('Invalid response data');
        }

        // Render widget
        this._renderWidget(container, data);

      } catch (error) {
        console.error('[ShebaWidget] Error:', error);
        this._renderError(container, error.message);
      }
    },

    /**
     * Render widget HTML
     * @private
     */
    _renderWidget: function(container, data) {
      const tips = (data.tips || []).slice(0, 3); // Max 3 tips
      const riskLevel = data.churn_score ? this._getRiskLevel(data.churn_score) : 'Standard';
      
      const html = `
        <div class="sheba-widget-container">
          <div class="sheba-widget">
            <div class="sheba-widget-header">
              <div class="sheba-widget-logo">👋</div>
              <div>
                <div class="sheba-widget-title">Hi, ${this._escapeHtml(data.customer_name)}!</div>
                <div class="sheba-widget-subtitle">${this._escapeHtml(data.engagement_level || 'Welcome')}</div>
              </div>
            </div>

            <div class="sheba-widget-stats">
              <div class="sheba-widget-stat">
                <div class="sheba-widget-stat-value">${data.loyalty_score || 0}</div>
                <div class="sheba-widget-stat-label">Loyalty Score</div>
              </div>
              <div class="sheba-widget-stat">
                <div class="sheba-widget-stat-value">${riskLevel}</div>
                <div class="sheba-widget-stat-label">Status</div>
              </div>
            </div>

            <div class="sheba-widget-section">
              <p style="margin: 0 0 12px 0; font-size: 14px; line-height: 1.5;">
                ${this._escapeHtml(data.risk_message || "We value your business!")}
              </p>
            </div>

            ${data.recommended_offer ? `
              <div class="sheba-widget-offer">
                🎁 <strong>Special Offer:</strong><br>
                ${this._escapeHtml(data.recommended_offer)}
              </div>
            ` : ''}

            ${tips.length > 0 ? `
              <div class="sheba-widget-section">
                <div class="sheba-widget-section-label">Pro Tips</div>
                <ul class="sheba-widget-tips">
                  ${tips.map(tip => `<li class="sheba-widget-tip">${this._escapeHtml(tip)}</li>`).join('')}
                </ul>
              </div>
            ` : ''}

            <button class="sheba-widget-button" onclick="window.ShebaWidget.handleClaim('${this._escapeHtml(data.customer_id || '')}')">
              Claim Offer →
            </button>
          </div>
        </div>
      `;

      container.innerHTML = html;
    },

    /**
     * Render error state
     * @private
     */
    _renderError: function(container, message) {
      const html = `
        <div class="sheba-widget-container">
          <div class="sheba-widget">
            <div class="sheba-widget-error">
              ⚠️ Unable to load widget<br>
              <small>${this._escapeHtml(message)}</small>
            </div>
          </div>
        </div>
      `;
      container.innerHTML = html;
    },

    /**
     * Get risk level label
     * @private
     */
    _getRiskLevel: function(score) {
      if (score >= 0.7) return '🔴 High';
      if (score >= 0.4) return '🟡 Medium';
      return '🟢 Low';
    },

    /**
     * Escape HTML to prevent XSS
     * @private
     */
    _escapeHtml: function(text) {
      const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
      };
      return text.replace(/[&<>"']/g, m => map[m]);
    },

    /**
     * Handle claim button click
     */
    handleClaim: function(customerId) {
      console.log('[ShebaWidget] Offer claimed for customer:', customerId);
      alert('✅ Thank you! Your offer has been activated. Check your email for details.');
      // In production, would send analytics/tracking event
    }
  };

  // Log that widget loaded
  console.log(`[ShebaWidget v${window.ShebaWidget.version}] Loaded and ready. Call ShebaWidget.init(config) to initialize.`);

})();
