"""
Customer Behavior Analyzer
Generates comprehensive behavior summaries and personalized recommendations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class CustomerBehaviorAnalyzer:
    """Analyzes customer behavior and generates actionable insights"""

    def __init__(self):
        self.industry_configs = self._load_industry_configs()

    def _load_industry_configs(self) -> Dict[str, Dict]:
        """Load industry-specific intervention configurations"""
        return {
            'ecommerce': {
                'high_risk': [
                    {
                        'condition': lambda c: c['total_value_90d'] > 500 and c['days_since_last_activity'] < 90,
                        'action': 'discount_voucher',
                        'params': {'amount_pct': 0.15, 'message': 'We miss you! Here\'s 15% off your next order'},
                        'channel': ['email', 'in_app']
                    },
                    {
                        'condition': lambda c: c['activity_trend'] < -0.3,
                        'action': 'personalized_recommendations',
                        'params': {'message': 'Products picked just for you'},
                        'channel': ['email']
                    }
                ],
                'medium_risk': [
                    {
                        'condition': lambda c: c['activity_count_90d'] > 0,
                        'action': 'loyalty_points_bonus',
                        'params': {'message': 'Earn 2x points this week'},
                        'channel': ['email', 'push']
                    }
                ]
            },
            'financial': {
                'high_risk': [
                    {
                        'condition': lambda c: c['tenure_days'] > 365 and c['activity_count_30d'] < 3,
                        'action': 'fee_waiver',
                        'params': {'duration_months': 3, 'message': 'Valued customer: 3 months fee-free'},
                        'channel': ['email', 'phone']
                    },
                    {
                        'condition': lambda c: c['support_tickets_30d'] > 2,
                        'action': 'relationship_manager_call',
                        'params': {'urgency': 'within_24h', 'message': 'Personal account manager will reach out'},
                        'channel': ['phone']
                    }
                ],
                'medium_risk': [
                    {
                        'condition': lambda c: c['feature_usage_count'] < 2,
                        'action': 'educational_content',
                        'params': {'type': 'tutorial', 'message': 'Discover features to make banking easier'},
                        'channel': ['email', 'in_app']
                    }
                ]
            },
            'saas': {
                'high_risk': [
                    {
                        'condition': lambda c: c['activity_trend'] < -0.4,
                        'action': 'plan_downgrade_offer',
                        'params': {'message': 'Switch to a plan that better fits your needs'},
                        'channel': ['email', 'in_app']
                    },
                    {
                        'condition': lambda c: c['support_tickets_30d'] > 3,
                        'action': 'technical_specialist_assignment',
                        'params': {'message': 'Dedicated technical support for your team'},
                        'channel': ['email', 'phone']
                    }
                ],
                'medium_risk': [
                    {
                        'condition': lambda c: c['session_count_30d'] < 10,
                        'action': 'onboarding_assistance',
                        'params': {'message': 'Let us help you get the most value'},
                        'channel': ['email', 'in_app']
                    }
                ]
            },
            'telecom': {
                'high_risk': [
                    {
                        'condition': lambda c: c['total_value_90d'] > 300,
                        'action': 'data_boost_offer',
                        'params': {'amount': '+10GB', 'discount': 0.20, 'message': '20% off + 10GB extra data'},
                        'channel': ['sms', 'email']
                    },
                    {
                        'condition': lambda c: c['support_tickets_30d'] > 2,
                        'action': 'technical_support_priority',
                        'params': {'message': 'Priority technical support assigned to your account'},
                        'channel': ['sms', 'phone']
                    }
                ]
            }
        }

    def generate_behavior_summary(
        self,
        customer_id: str,
        customer_data: pd.Series,
        churn_risk_score: float,
        segment: str,
        customer_type: Optional[str] = None,
        industry: str = 'ecommerce'
    ) -> Dict[str, Any]:
        """
        Generate comprehensive behavior summary for a customer.

        Args:
            customer_id: Customer identifier
            customer_data: Customer feature data
            churn_risk_score: Churn risk score (0-100)
            segment: RFM segment
            customer_type: Uplift model customer type (Persuadable, etc.)
            industry: Industry type for personalized recommendations

        Returns:
            Comprehensive behavior summary dictionary
        """
        summary = {
            'customer_id': customer_id,
            'profile': self._analyze_profile(customer_data, segment),
            'engagement': self._analyze_engagement(customer_data),
            'value': self._analyze_value(customer_data),
            'trends': self._analyze_trends(customer_data),
            'risk_indicators': self._identify_risk_indicators(customer_data, churn_risk_score),
            'recommendations': self._generate_recommendations(
                customer_data,
                churn_risk_score,
                segment,
                customer_type,
                industry
            ),
            'churn_risk_score': churn_risk_score,
            'segment': segment,
            'customer_type': customer_type
        }

        return summary

    def _analyze_profile(self, data: pd.Series, segment: str) -> Dict[str, Any]:
        """Analyze customer profile"""
        return {
            'segment': segment,
            'tenure': f"{int(data['tenure_days'])} days ({int(data['tenure_days']/30)} months)",
            'lifecycle_stage': self._determine_lifecycle_stage(data['tenure_days']),
            'customer_type': self._determine_customer_type_description(data)
        }

    def _analyze_engagement(self, data: pd.Series) -> Dict[str, Any]:
        """Analyze engagement patterns"""
        return {
            'activity_level': self._categorize_activity(data['activity_count_90d']),
            'last_active': f"{int(data['days_since_last_activity'])} days ago",
            'avg_frequency': f"{data['activity_count_30d']:.1f} activities/month",
            'engagement_score': f"{data['engagement_score']:.1f}/100",
            'engagement_trend': self._describe_trend(data['activity_trend']),
            'session_activity': f"{int(data['session_count_30d'])} sessions in last 30 days"
        }

    def _analyze_value(self, data: pd.Series) -> Dict[str, Any]:
        """Analyze customer value"""
        return {
            'total_value_90d': f"${data['total_value_90d']:.2f}",
            'total_value_30d': f"${data['total_value_30d']:.2f}",
            'avg_transaction': f"${data['avg_value_per_activity']:.2f}",
            'value_segment': self._categorize_value(data['monetary_score']),
            'monthly_average': f"${data['total_value_30d']:.2f}/month"
        }

    def _analyze_trends(self, data: pd.Series) -> List[str]:
        """Identify behavioral trends"""
        trends = []

        if data['activity_trend'] < -0.2:
            trends.append("⚠️ Declining activity over recent period")
        elif data['activity_trend'] > 0.2:
            trends.append("📈 Increasing engagement")

        if data['days_since_last_activity'] > 60:
            trends.append("🔴 Extended inactivity period")
        elif data['days_since_last_activity'] < 7:
            trends.append("🟢 Recently active")

        if data['recency_score'] < 3 and data['monetary_score'] >= 4:
            trends.append("💰 High-value but disengaging")

        if data['support_tickets_30d'] > 2:
            trends.append("⚠️ Multiple support interactions")

        if data['satisfaction_score'] < 50:
            trends.append("😟 Low satisfaction signals")
        elif data['satisfaction_score'] > 80:
            trends.append("😊 High satisfaction")

        if data['payment_failures'] > 0:
            trends.append("💳 Recent payment issues")

        return trends if trends else ["📊 Stable behavior patterns"]

    def _identify_risk_indicators(self, data: pd.Series, churn_risk_score: float) -> List[Dict[str, str]]:
        """Identify churn risk indicators"""
        indicators = []

        if churn_risk_score > 70:
            indicators.append({
                'type': 'Critical',
                'indicator': 'Very high churn probability',
                'action': 'Immediate intervention required',
                'priority': 'High'
            })

        if data['days_since_last_activity'] > 90:
            indicators.append({
                'type': 'Warning',
                'indicator': 'No activity for 3+ months',
                'action': 'Re-engagement campaign recommended',
                'priority': 'High'
            })

        if data['activity_trend'] < -0.3:
            indicators.append({
                'type': 'Warning',
                'indicator': 'Significant decline in engagement',
                'action': 'Proactive outreach needed',
                'priority': 'Medium'
            })

        if data['frequency_score'] < 2:
            indicators.append({
                'type': 'Warning',
                'indicator': 'Low activity frequency',
                'action': 'Increase touchpoints and incentives',
                'priority': 'Medium'
            })

        if data['support_tickets_30d'] > 3:
            indicators.append({
                'type': 'Warning',
                'indicator': 'High support ticket volume',
                'action': 'Address underlying issues',
                'priority': 'High'
            })

        if data['satisfaction_score'] < 40:
            indicators.append({
                'type': 'Critical',
                'indicator': 'Very low satisfaction',
                'action': 'Service recovery intervention',
                'priority': 'Critical'
            })

        if not indicators:
            indicators.append({
                'type': 'Info',
                'indicator': 'No significant risk indicators',
                'action': 'Continue monitoring',
                'priority': 'Low'
            })

        return indicators

    def _generate_recommendations(
        self,
        data: pd.Series,
        churn_risk_score: float,
        segment: str,
        customer_type: Optional[str],
        industry: str
    ) -> List[Dict[str, Any]]:
        """Generate personalized recommendations"""
        recommendations = []

        # Critical churn risk recommendations
        if churn_risk_score > 70:
            if customer_type != 'Lost Cause':  # Only if intervention can help
                recommendations.append({
                    'priority': 'Critical',
                    'action': 'Personal outreach from account manager',
                    'reason': 'Critical churn risk detected',
                    'expected_impact': 'High',
                    'timing': 'Immediate'
                })

                if data['monetary_score'] >= 3:
                    recommendations.append({
                        'priority': 'Critical',
                        'action': 'Offer retention incentive (15-20% value)',
                        'reason': 'Prevent imminent churn of valuable customer',
                        'expected_impact': 'High',
                        'timing': 'Within 24 hours'
                    })

        # Segment-specific recommendations
        if segment == "Champions":
            recommendations.append({
                'priority': 'Medium',
                'action': 'Enroll in VIP loyalty program',
                'reason': 'Reward and retain top customers',
                'expected_impact': 'Medium',
                'timing': 'Within 1 week'
            })

        elif segment == "At Risk" or segment == "Can't Lose Them":
            recommendations.append({
                'priority': 'High',
                'action': 'Win-back campaign with special offer',
                'reason': 'Re-engage valuable at-risk customer',
                'expected_impact': 'High',
                'timing': 'Immediate'
            })

        elif segment == "New Customers":
            recommendations.append({
                'priority': 'Medium',
                'action': 'Onboarding and education sequence',
                'reason': 'Build engagement with new customer',
                'expected_impact': 'Medium',
                'timing': 'Within 3 days'
            })

        # Activity-based recommendations
        if data['frequency_score'] < 3:
            recommendations.append({
                'priority': 'Medium',
                'action': 'Send personalized product/content recommendations',
                'reason': 'Increase engagement frequency',
                'expected_impact': 'Medium',
                'timing': 'Within 1 week'
            })

        # Support-based recommendations
        if data['support_tickets_30d'] > 2:
            recommendations.append({
                'priority': 'High',
                'action': 'Assign dedicated support specialist',
                'reason': 'Address recurring issues proactively',
                'expected_impact': 'High',
                'timing': 'Within 24 hours'
            })

        # Industry-specific recommendations
        industry_recs = self._get_industry_specific_recommendations(data, churn_risk_score, industry)
        recommendations.extend(industry_recs)

        # Customer type specific (from uplift modeling)
        if customer_type == 'Sleeping Dog':
            recommendations.append({
                'priority': 'Critical',
                'action': 'DO NOT CONTACT - May trigger churn',
                'reason': 'Customer shows negative response to interventions',
                'expected_impact': 'Negative if contacted',
                'timing': 'N/A'
            })

        # Sort by priority
        priority_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 999))

        return recommendations[:5]  # Return top 5 recommendations

    def _get_industry_specific_recommendations(
        self,
        data: pd.Series,
        churn_risk_score: float,
        industry: str
    ) -> List[Dict[str, Any]]:
        """Get industry-specific recommendations"""
        recommendations = []

        if industry not in self.industry_configs:
            return recommendations

        config = self.industry_configs[industry]

        # Check high risk interventions
        if churn_risk_score > 70 and 'high_risk' in config:
            for intervention in config['high_risk']:
                try:
                    if intervention['condition'](data):
                        recommendations.append({
                            'priority': 'High',
                            'action': intervention['action'],
                            'reason': f"Industry best practice for {industry}",
                            'params': intervention['params'],
                            'channel': intervention['channel'],
                            'expected_impact': 'High',
                            'timing': 'Immediate'
                        })
                        break  # Only add first matching intervention
                except Exception as e:
                    logger.warning(f"Error evaluating condition: {e}")

        # Check medium risk interventions
        elif churn_risk_score > 40 and 'medium_risk' in config:
            for intervention in config['medium_risk']:
                try:
                    if intervention['condition'](data):
                        recommendations.append({
                            'priority': 'Medium',
                            'action': intervention['action'],
                            'reason': f"Industry best practice for {industry}",
                            'params': intervention['params'],
                            'channel': intervention['channel'],
                            'expected_impact': 'Medium',
                            'timing': 'Within 1 week'
                        })
                        break
                except Exception as e:
                    logger.warning(f"Error evaluating condition: {e}")

        return recommendations

    def _determine_lifecycle_stage(self, tenure_days: int) -> str:
        """Determine customer lifecycle stage"""
        if tenure_days < 30:
            return "New"
        elif tenure_days < 180:
            return "Growing"
        elif tenure_days < 365:
            return "Mature"
        else:
            return "Loyal"

    def _determine_customer_type_description(self, data: pd.Series) -> str:
        """Determine customer type based on behavior"""
        if data['engagement_score'] > 80:
            return "Highly Engaged"
        elif data['engagement_score'] > 60:
            return "Engaged"
        elif data['engagement_score'] > 40:
            return "Moderately Engaged"
        else:
            return "Low Engagement"

    def _categorize_activity(self, frequency: int) -> str:
        """Categorize activity level"""
        if frequency >= 20:
            return "Very Active"
        elif frequency >= 10:
            return "Active"
        elif frequency >= 5:
            return "Moderate"
        else:
            return "Low"

    def _categorize_value(self, monetary_score: int) -> str:
        """Categorize customer value"""
        if monetary_score >= 5:
            return "High Value"
        elif monetary_score >= 3:
            return "Medium Value"
        else:
            return "Low Value"

    def _describe_trend(self, trend_value: float) -> str:
        """Describe trend direction"""
        if trend_value > 0.2:
            return "Increasing ↗"
        elif trend_value < -0.2:
            return "Decreasing ↘"
        else:
            return "Stable →"

    def format_summary_for_api(self, summary: Dict[str, Any]) -> Dict[str, Any]:
        """Format summary for API response"""
        return {
            'customer_id': summary['customer_id'],
            'churn_risk_score': round(summary['churn_risk_score'], 2),
            'segment': summary['segment'],
            'customer_type': summary.get('customer_type', 'Unknown'),
            'profile': summary['profile'],
            'engagement': summary['engagement'],
            'value': summary['value'],
            'insights': {
                'trends': summary['trends'],
                'risk_indicators': summary['risk_indicators']
            },
            'recommendations': summary['recommendations'],
            'generated_at': datetime.now().isoformat()
        }

    def batch_analyze(
        self,
        customers_df: pd.DataFrame,
        churn_scores: pd.Series,
        segments: pd.Series,
        customer_types: Optional[pd.Series] = None,
        industry: str = 'ecommerce'
    ) -> List[Dict[str, Any]]:
        """Batch analyze multiple customers"""
        logger.info(f"Batch analyzing {len(customers_df)} customers...")

        summaries = []

        for idx, customer in customers_df.iterrows():
            customer_id = customer['customer_id']
            churn_score = churn_scores.loc[idx]
            segment = segments.loc[idx]
            customer_type = customer_types.loc[idx] if customer_types is not None else None

            summary = self.generate_behavior_summary(
                customer_id,
                customer,
                churn_score,
                segment,
                customer_type,
                industry
            )

            summaries.append(summary)

        logger.info(f"Completed batch analysis of {len(summaries)} customers")

        return summaries
