"""
Schema Mapper: Normalizes different dataset formats to universal RFM schema
Handles: Criteo, Hillstrom, Financial Services, B2B datasets
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class UnitNormalizer:
    """Handles unit conversions and normalization"""

    @staticmethod
    def normalize_time_units(value: float, source_unit: str) -> float:
        """Convert time to days"""
        conversions = {
            'seconds': 1/86400,
            'minutes': 1/1440,
            'hours': 1/24,
            'days': 1,
            'weeks': 7,
            'months': 30,
            'years': 365
        }
        return value * conversions.get(source_unit.lower(), 1)

    @staticmethod
    def normalize_monetary_units(value: float, currency: str = 'USD') -> float:
        """Convert currency to USD (simplified - use forex API in production)"""
        # Simplified conversion rates
        rates = {
            'USD': 1.0,
            'EUR': 1.1,
            'GBP': 1.3,
            'BDT': 0.0091,  # Bangladeshi Taka
            'INR': 0.012,
            'JPY': 0.0067
        }
        return value * rates.get(currency.upper(), 1.0)

    @staticmethod
    def detect_time_unit(values: pd.Series, column_name: str) -> str:
        """Auto-detect time unit based on value ranges and column name"""
        max_val = values.max()

        # Check column name for hints
        name_lower = column_name.lower()
        if 'second' in name_lower:
            return 'seconds'
        if 'minute' in name_lower or 'min' in name_lower:
            return 'minutes'
        if 'hour' in name_lower or 'hr' in name_lower:
            return 'hours'
        if 'day' in name_lower:
            return 'days'
        if 'week' in name_lower:
            return 'weeks'
        if 'month' in name_lower:
            return 'months'

        # Heuristic based on value ranges
        if max_val < 60:
            return 'minutes'
        elif max_val < 1440:  # 24 * 60
            return 'minutes'
        elif max_val < 720:  # 30 * 24
            return 'hours'
        elif max_val < 365:
            return 'days'
        else:
            return 'days'


class SchemaMapper:
    """Maps different dataset schemas to universal RFM schema"""

    def __init__(self):
        self.unit_normalizer = UnitNormalizer()

    def map_criteo(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Map Criteo dataset to universal schema.

        Criteo Dataset Structure:
        - f0-f11: 12 anonymized features (dense, continuous)
        - treatment: {0, 1} - 1 = ad shown, 0 = control
        - exposure: {0, 1} - Actually saw the ad
        - visit: {0, 1} - Visited website
        - conversion: {0, 1} - Made purchase (outcome)
        """
        logger.info("Mapping Criteo dataset to universal schema")

        normalized_df = pd.DataFrame()

        # Generate customer IDs
        normalized_df['customer_id'] = df.index.astype(str)

        # Treatment and Outcome
        normalized_df['treatment'] = df['treatment']
        normalized_df['treatment_type'] = df['treatment'].apply(lambda x: 'ad_campaign' if x == 1 else 'control')
        normalized_df['outcome'] = 1 - df['conversion']  # 1 = churned (didn't convert), 0 = retained (converted)

        # RFM-like features from Criteo's anonymized features
        # f0-f11 are anonymized, so we'll use them as proxy features
        # Typically, Criteo features represent user behavior metrics

        # Use f0-f3 for recency proxies
        normalized_df['days_since_last_activity'] = df['f0'].clip(lower=0)

        # Use f4-f7 for frequency proxies
        normalized_df['activity_count_30d'] = df['f4'].clip(lower=0).astype(int)
        normalized_df['activity_count_90d'] = df['f5'].clip(lower=0).astype(int)

        # Use f8-f11 for monetary proxies
        normalized_df['total_value_30d'] = df['f8'].clip(lower=0)
        normalized_df['total_value_90d'] = df['f9'].clip(lower=0)
        normalized_df['avg_value_per_activity'] = df['f10'].clip(lower=0)

        # Additional behavioral features
        normalized_df['tenure_days'] = df['f1'].clip(lower=1).astype(int)
        normalized_df['engagement_score'] = df['f2'].clip(0, 100)
        normalized_df['activity_trend'] = df['f3']  # % change
        normalized_df['feature_usage_count'] = df['f6'].clip(lower=0).astype(int)
        normalized_df['session_count_30d'] = df['f7'].clip(lower=0).astype(int)

        # Support/Service (use remaining features or defaults)
        normalized_df['support_tickets_30d'] = 0  # Not available in Criteo
        normalized_df['satisfaction_score'] = 75.0  # Default neutral score

        # Financial
        normalized_df['payment_failures'] = 0
        normalized_df['account_balance'] = df['f11'].clip(lower=0)

        # Calculate RFM scores
        normalized_df = self._calculate_rfm_scores(normalized_df)

        # Store original data
        normalized_df['original_data'] = df.to_dict('records')

        mapping_info = {
            'dataset_type': 'criteo',
            'mapped_columns': {
                'treatment': 'treatment',
                'outcome': '1 - conversion',
                'recency': 'f0',
                'frequency': 'f4, f5',
                'monetary': 'f8, f9, f10',
                'behavioral': 'f1, f2, f3, f6, f7',
                'financial': 'f11'
            },
            'total_records': len(df),
            'treatment_count': df['treatment'].sum(),
            'control_count': len(df) - df['treatment'].sum()
        }

        return normalized_df, mapping_info

    def map_hillstrom(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Map Hillstrom email marketing dataset to universal schema.

        Hillstrom Dataset Structure:
        - recency: Months since last purchase
        - history: Total spend in past 12 months
        - mens: Received men's email (treatment 1)
        - womens: Received women's email (treatment 2)
        - zip_code: Geographic info
        - newbie: New vs returning customer
        - channel: Acquisition channel (Phone/Web/Multichannel)
        - visit: Visited within 2 weeks (outcome)
        - conversion: Made purchase (outcome)
        - spend: Amount spent (outcome)
        """
        logger.info("Mapping Hillstrom dataset to universal schema")

        normalized_df = pd.DataFrame()

        # Generate or use existing customer IDs
        if 'customer_id' in df.columns:
            normalized_df['customer_id'] = df['customer_id'].astype(str)
        else:
            normalized_df['customer_id'] = df.index.astype(str)

        # Treatment and Outcome
        # Combine mens and womens into single treatment flag
        normalized_df['treatment'] = ((df['mens'] == 1) | (df['womens'] == 1)).astype(int)
        normalized_df['treatment_type'] = df.apply(
            lambda row: 'mens_email' if row.get('mens', 0) == 1 else (
                'womens_email' if row.get('womens', 0) == 1 else 'control'
            ), axis=1
        )
        normalized_df['outcome'] = 1 - df['conversion']  # 1 = churned (didn't convert), 0 = retained (converted)

        # RFM Features
        # Recency: months since last purchase -> convert to days
        normalized_df['days_since_last_activity'] = (df['recency'] * 30).astype(int)

        # Frequency: derive from history and spend patterns
        # Assume average order value to estimate frequency
        avg_order_value = df['history'].quantile(0.5) / 4  # Assume ~4 purchases per year on average
        normalized_df['activity_count_90d'] = (df['history'] / avg_order_value / 4).clip(lower=0).astype(int)
        normalized_df['activity_count_30d'] = (normalized_df['activity_count_90d'] / 3).astype(int)

        # Monetary
        normalized_df['total_value_90d'] = df['history'] / 4  # Last 3 months of 12-month history
        normalized_df['total_value_30d'] = df['history'] / 12
        normalized_df['avg_value_per_activity'] = df['history'] / normalized_df['activity_count_90d'].replace(0, 1)

        # Behavioral features
        normalized_df['tenure_days'] = df.apply(
            lambda row: 30 if row['newbie'] == 1 else 365, axis=1
        )
        normalized_df['engagement_score'] = df.apply(
            lambda row: self._calculate_engagement_score(
                row['recency'],
                normalized_df.loc[row.name, 'activity_count_90d'],
                row['history']
            ), axis=1
        )
        normalized_df['activity_trend'] = df.apply(
            lambda row: -0.3 if row['recency'] > 6 else (0.2 if row['recency'] < 3 else 0.0), axis=1
        )
        normalized_df['feature_usage_count'] = df['channel'].apply(
            lambda x: 3 if x == 'Multichannel' else (2 if x == 'Web' else 1)
        )
        normalized_df['session_count_30d'] = normalized_df['activity_count_30d'] * 2

        # Support/Service
        normalized_df['support_tickets_30d'] = 0  # Not available
        normalized_df['satisfaction_score'] = df.apply(
            lambda row: 80.0 if row['recency'] < 3 else (60.0 if row['recency'] < 6 else 40.0), axis=1
        )

        # Financial
        normalized_df['payment_failures'] = 0
        normalized_df['account_balance'] = df['history']  # Use total history as proxy

        # Calculate RFM scores
        normalized_df = self._calculate_rfm_scores(normalized_df)

        # Store original data
        normalized_df['original_data'] = df.to_dict('records')

        mapping_info = {
            'dataset_type': 'hillstrom',
            'mapped_columns': {
                'treatment': 'mens OR womens',
                'outcome': '1 - conversion',
                'recency': 'recency (months -> days)',
                'frequency': 'derived from history',
                'monetary': 'history',
                'channel': 'channel'
            },
            'total_records': len(df),
            'treatment_count': int(normalized_df['treatment'].sum()),
            'control_count': int(len(df) - normalized_df['treatment'].sum())
        }

        return normalized_df, mapping_info

    def map_financial(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Map Financial Services dataset to universal schema.

        Expected columns (flexible):
        - customer_id
        - treatment: Targeted in retention campaign
        - churned: Churned in observation window
        - age, gender, account_balance, transaction_count_30d
        - avg_transaction_value, products_owned, tenure_months
        - last_login_days, support_tickets_90d, credit_score
        + 150+ additional features
        """
        logger.info("Mapping Financial Services dataset to universal schema")

        normalized_df = pd.DataFrame()

        # Customer ID
        if 'customer_id' in df.columns:
            normalized_df['customer_id'] = df['customer_id'].astype(str)
        else:
            normalized_df['customer_id'] = df.index.astype(str)

        # Treatment and Outcome
        normalized_df['treatment'] = df.get('treatment', 0)
        normalized_df['treatment_type'] = df.get('treatment_type',
                                                  df['treatment'].apply(lambda x: 'retention_campaign' if x == 1 else 'control'))
        normalized_df['outcome'] = df.get('churned', 0)

        # RFM Features
        # Recency
        if 'last_login_days' in df.columns:
            normalized_df['days_since_last_activity'] = df['last_login_days']
        elif 'days_since_last_transaction' in df.columns:
            normalized_df['days_since_last_activity'] = df['days_since_last_transaction']
        else:
            normalized_df['days_since_last_activity'] = 30  # Default

        # Frequency
        normalized_df['activity_count_30d'] = df.get('transaction_count_30d',
                                                       df.get('transactions_30d', 5))
        normalized_df['activity_count_90d'] = df.get('transaction_count_90d',
                                                       normalized_df['activity_count_30d'] * 3)

        # Monetary
        normalized_df['total_value_30d'] = df.get('total_transaction_value_30d',
                                                    df.get('avg_transaction_value', 100) * normalized_df['activity_count_30d'])
        normalized_df['total_value_90d'] = df.get('total_transaction_value_90d',
                                                    normalized_df['total_value_30d'] * 3)
        normalized_df['avg_value_per_activity'] = df.get('avg_transaction_value',
                                                           normalized_df['total_value_30d'] / normalized_df['activity_count_30d'].replace(0, 1))

        # Behavioral features
        normalized_df['tenure_days'] = df.get('tenure_months', 12) * 30
        normalized_df['engagement_score'] = df.apply(
            lambda row: self._calculate_engagement_score(
                normalized_df.loc[row.name, 'days_since_last_activity'],
                normalized_df.loc[row.name, 'activity_count_90d'],
                normalized_df.loc[row.name, 'total_value_90d']
            ), axis=1
        )

        # Activity trend: calculate from recent vs historical activity
        if 'transaction_count_previous_90d' in df.columns:
            normalized_df['activity_trend'] = (
                (normalized_df['activity_count_90d'] - df['transaction_count_previous_90d']) /
                df['transaction_count_previous_90d'].replace(0, 1)
            )
        else:
            # Estimate based on recency
            normalized_df['activity_trend'] = normalized_df['days_since_last_activity'].apply(
                lambda x: -0.4 if x > 60 else (-0.2 if x > 30 else 0.1)
            )

        normalized_df['feature_usage_count'] = df.get('products_owned', 2)
        normalized_df['session_count_30d'] = df.get('mobile_banking_logins',
                                                      normalized_df['activity_count_30d'])

        # Support/Service
        normalized_df['support_tickets_30d'] = df.get('support_tickets_30d',
                                                        df.get('support_tickets_90d', 0) / 3)
        normalized_df['satisfaction_score'] = df.get('satisfaction_score',
                                                       df.get('nps_score', 70.0))

        # Financial
        normalized_df['payment_failures'] = df.get('payment_failures',
                                                     df.get('overdraft_count', 0))
        normalized_df['account_balance'] = df.get('account_balance',
                                                    df.get('checking_balance', 1000.0))

        # Calculate RFM scores
        normalized_df = self._calculate_rfm_scores(normalized_df)

        # Store original data
        normalized_df['original_data'] = df.to_dict('records')

        mapping_info = {
            'dataset_type': 'financial',
            'mapped_columns': {
                'treatment': 'treatment',
                'outcome': 'churned',
                'recency': 'last_login_days or days_since_last_transaction',
                'frequency': 'transaction_count_30d, transaction_count_90d',
                'monetary': 'transaction_value fields',
                'tenure': 'tenure_months'
            },
            'total_records': len(df),
            'treatment_count': int(normalized_df['treatment'].sum()),
            'control_count': int(len(df) - normalized_df['treatment'].sum())
        }

        return normalized_df, mapping_info

    def map_b2b(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Map B2B SaaS dataset to universal schema.

        Expected columns:
        - customer_id
        - treatment: Called by retention team
        - churned: Canceled subscription
        - contract_value_per_month, contract_duration_months
        - feature_usage_count, support_tickets
        - user_seats, industry, company_size
        - days_since_last_login
        """
        logger.info("Mapping B2B SaaS dataset to universal schema")

        normalized_df = pd.DataFrame()

        # Customer ID
        if 'customer_id' in df.columns:
            normalized_df['customer_id'] = df['customer_id'].astype(str)
        else:
            normalized_df['customer_id'] = df.index.astype(str)

        # Treatment and Outcome
        normalized_df['treatment'] = df.get('treatment', 0)
        normalized_df['treatment_type'] = df.get('treatment_type',
                                                  df['treatment'].apply(lambda x: 'retention_call' if x == 1 else 'control'))
        normalized_df['outcome'] = df.get('churned', 0)

        # RFM Features for B2B
        # Recency: days since last login/usage
        normalized_df['days_since_last_activity'] = df.get('days_since_last_login',
                                                             df.get('days_since_last_usage', 7))

        # Frequency: feature usage, API calls, logins
        normalized_df['activity_count_30d'] = df.get('feature_usage_count',
                                                       df.get('api_calls_30d', 50))
        normalized_df['activity_count_90d'] = normalized_df['activity_count_30d'] * 3

        # Monetary: contract value
        normalized_df['total_value_30d'] = df.get('contract_value_per_month', 500)
        normalized_df['total_value_90d'] = normalized_df['total_value_30d'] * 3
        normalized_df['avg_value_per_activity'] = (
            normalized_df['total_value_30d'] /
            normalized_df['activity_count_30d'].replace(0, 1)
        )

        # Behavioral features
        normalized_df['tenure_days'] = df.get('contract_duration_months', 6) * 30

        # Engagement score based on seat utilization and feature usage
        if 'seats_active' in df.columns and 'seats_purchased' in df.columns:
            seat_utilization = df['seats_active'] / df['seats_purchased'].replace(0, 1)
        else:
            seat_utilization = 0.75  # Default

        normalized_df['engagement_score'] = df.apply(
            lambda row: self._calculate_b2b_engagement_score(
                normalized_df.loc[row.name, 'days_since_last_activity'],
                normalized_df.loc[row.name, 'activity_count_30d'],
                seat_utilization if isinstance(seat_utilization, float) else seat_utilization.loc[row.name]
            ), axis=1
        )

        # Activity trend
        if 'feature_usage_previous_30d' in df.columns:
            normalized_df['activity_trend'] = (
                (normalized_df['activity_count_30d'] - df['feature_usage_previous_30d']) /
                df['feature_usage_previous_30d'].replace(0, 1)
            )
        else:
            normalized_df['activity_trend'] = normalized_df['days_since_last_activity'].apply(
                lambda x: -0.5 if x > 14 else (0.2 if x < 3 else 0.0)
            )

        normalized_df['feature_usage_count'] = df.get('feature_usage_count',
                                                        df.get('integrations_enabled', 5))
        normalized_df['session_count_30d'] = df.get('admin_logins_30d', 20)

        # Support/Service
        normalized_df['support_tickets_30d'] = df.get('support_tickets',
                                                        df.get('support_tickets_30d', 1))
        normalized_df['satisfaction_score'] = df.get('csat_score',
                                                       df.get('nps_score', 75.0))

        # Financial
        normalized_df['payment_failures'] = df.get('payment_failures', 0)
        normalized_df['account_balance'] = df.get('account_balance',
                                                    normalized_df['total_value_90d'])

        # Calculate RFM scores
        normalized_df = self._calculate_rfm_scores(normalized_df)

        # Store original data
        normalized_df['original_data'] = df.to_dict('records')

        mapping_info = {
            'dataset_type': 'b2b',
            'mapped_columns': {
                'treatment': 'treatment',
                'outcome': 'churned',
                'recency': 'days_since_last_login or days_since_last_usage',
                'frequency': 'feature_usage_count or api_calls_30d',
                'monetary': 'contract_value_per_month',
                'tenure': 'contract_duration_months'
            },
            'total_records': len(df),
            'treatment_count': int(normalized_df['treatment'].sum()),
            'control_count': int(len(df) - normalized_df['treatment'].sum())
        }

        return normalized_df, mapping_info

    def _calculate_rfm_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate RFM scores using quintile method"""

        # Recency Score (lower is better, so reverse)
        df['recency_score'] = pd.qcut(
            df['days_since_last_activity'],
            q=5,
            labels=[5, 4, 3, 2, 1],
            duplicates='drop'
        ).astype(int)

        # Frequency Score
        df['frequency_score'] = pd.qcut(
            df['activity_count_90d'].rank(method='first'),
            q=5,
            labels=[1, 2, 3, 4, 5],
            duplicates='drop'
        ).astype(int)

        # Monetary Score
        df['monetary_score'] = pd.qcut(
            df['total_value_90d'].rank(method='first'),
            q=5,
            labels=[1, 2, 3, 4, 5],
            duplicates='drop'
        ).astype(int)

        # Combined RFM Score
        df['rfm_score'] = df['recency_score'] + df['frequency_score'] + df['monetary_score']

        return df

    def _calculate_engagement_score(self, recency: float, frequency: int, monetary: float) -> float:
        """Calculate engagement score (0-100)"""
        # Normalize components
        recency_score = max(0, 100 - (recency / 90 * 100))  # 0 days = 100, 90+ days = 0
        frequency_score = min(100, (frequency / 10) * 100)  # 10+ activities = 100
        monetary_score = min(100, (monetary / 1000) * 100)  # $1000+ = 100

        # Weighted average
        engagement = (recency_score * 0.4 + frequency_score * 0.3 + monetary_score * 0.3)
        return round(engagement, 2)

    def _calculate_b2b_engagement_score(self, recency: float, frequency: int, seat_utilization: float) -> float:
        """Calculate B2B-specific engagement score"""
        recency_score = max(0, 100 - (recency / 30 * 100))  # 0 days = 100, 30+ days = 0
        frequency_score = min(100, (frequency / 100) * 100)  # 100+ activities = 100
        utilization_score = seat_utilization * 100

        # Weighted for B2B
        engagement = (recency_score * 0.3 + frequency_score * 0.3 + utilization_score * 0.4)
        return round(engagement, 2)

    def auto_detect_and_map(self, df: pd.DataFrame, dataset_type: Optional[str] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Auto-detect dataset type and map accordingly"""

        if dataset_type:
            dataset_type = dataset_type.lower()
        else:
            # Auto-detect based on columns
            columns = set(df.columns)

            if 'treatment' in columns and 'conversion' in columns and any(f'f{i}' in columns for i in range(12)):
                dataset_type = 'criteo'
            elif 'recency' in columns and 'history' in columns and 'mens' in columns:
                dataset_type = 'hillstrom'
            elif 'contract_value_per_month' in columns or 'feature_usage_count' in columns:
                dataset_type = 'b2b'
            elif 'account_balance' in columns or 'credit_score' in columns:
                dataset_type = 'financial'
            else:
                dataset_type = 'financial'  # Default fallback

        logger.info(f"Auto-detected dataset type: {dataset_type}")

        # Map based on type
        if dataset_type == 'criteo':
            return self.map_criteo(df)
        elif dataset_type == 'hillstrom':
            return self.map_hillstrom(df)
        elif dataset_type == 'financial':
            return self.map_financial(df)
        elif dataset_type == 'b2b':
            return self.map_b2b(df)
        else:
            raise ValueError(f"Unknown dataset type: {dataset_type}")
