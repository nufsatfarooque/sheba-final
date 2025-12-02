"""
Uplift Modeling: Predicts treatment effects for personalized interventions
Uses X-Learner and Causal Forest approaches
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import logging
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import joblib
from pathlib import Path

logger = logging.getLogger(__name__)


class XLearner:
    """
    X-Learner for uplift modeling.
    Effective when treatment and control groups are imbalanced.
    """

    def __init__(self):
        # Stage 1: Response models
        self.model_treatment = GradientBoostingClassifier(n_estimators=100, random_state=42)
        self.model_control = GradientBoostingClassifier(n_estimators=100, random_state=42)

        # Stage 2: Treatment effect models
        self.model_tau_treatment = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model_tau_control = RandomForestClassifier(n_estimators=100, random_state=42)

        # Propensity model
        self.propensity_model = LogisticRegression(max_iter=1000, random_state=42)

        self.is_fitted = False
        self.feature_names = None

    def fit(self, X: pd.DataFrame, treatment: np.ndarray, y: np.ndarray):
        """
        Fit the X-Learner model.

        Args:
            X: Feature matrix
            treatment: Treatment indicator (0 or 1)
            y: Outcome (0 = retained, 1 = churned)
        """
        logger.info("Training X-Learner model...")

        self.feature_names = X.columns.tolist()

        # Split by treatment group
        X_treatment = X[treatment == 1]
        y_treatment = y[treatment == 1]
        X_control = X[treatment == 0]
        y_control = y[treatment == 0]

        # Stage 1: Fit response models
        logger.info("Stage 1: Training response models...")
        self.model_treatment.fit(X_treatment, y_treatment)
        self.model_control.fit(X_control, y_control)

        # Stage 2: Impute treatment effects
        logger.info("Stage 2: Computing imputed treatment effects...")

        # Predict what would have happened to treatment group under control
        mu_control_on_treatment = self.model_control.predict_proba(X_treatment)[:, 1]
        # Imputed treatment effect for treatment group
        tau_treatment = y_treatment - mu_control_on_treatment

        # Predict what would have happened to control group under treatment
        mu_treatment_on_control = self.model_treatment.predict_proba(X_control)[:, 1]
        # Imputed treatment effect for control group
        tau_control = mu_treatment_on_control - y_control

        # Stage 3: Fit treatment effect models
        logger.info("Stage 3: Training treatment effect models...")
        self.model_tau_treatment.fit(X_treatment, tau_treatment)
        self.model_tau_control.fit(X_control, tau_control)

        # Fit propensity model
        logger.info("Training propensity model...")
        self.propensity_model.fit(X, treatment)

        self.is_fitted = True
        logger.info("X-Learner training completed!")

    def predict_uplift(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict uplift (treatment effect) for new data.

        Returns:
            Uplift scores (positive = treatment helps, negative = treatment harms)
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")

        # Get propensity scores
        propensity = self.propensity_model.predict_proba(X)[:, 1]

        # Get treatment effect predictions from both models
        tau_treatment_pred = self.model_tau_treatment.predict(X)
        tau_control_pred = self.model_tau_control.predict(X)

        # Weighted average based on propensity
        # When propensity is high (more likely to be treated), trust treatment model more
        uplift = propensity * tau_control_pred + (1 - propensity) * tau_treatment_pred

        return uplift

    def predict_churn_probability(self, X: pd.DataFrame, treatment_value: int = 1) -> np.ndarray:
        """
        Predict probability of churn under treatment or control.

        Args:
            X: Features
            treatment_value: 1 for treatment, 0 for control

        Returns:
            Predicted churn probabilities
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")

        if treatment_value == 1:
            return self.model_treatment.predict_proba(X)[:, 1]
        else:
            return self.model_control.predict_proba(X)[:, 1]

    def save(self, path: str):
        """Save model to disk"""
        model_data = {
            'model_treatment': self.model_treatment,
            'model_control': self.model_control,
            'model_tau_treatment': self.model_tau_treatment,
            'model_tau_control': self.model_tau_control,
            'propensity_model': self.propensity_model,
            'feature_names': self.feature_names,
            'is_fitted': self.is_fitted
        }
        joblib.dump(model_data, path)
        logger.info(f"Model saved to {path}")

    def load(self, path: str):
        """Load model from disk"""
        model_data = joblib.load(path)
        self.model_treatment = model_data['model_treatment']
        self.model_control = model_data['model_control']
        self.model_tau_treatment = model_data['model_tau_treatment']
        self.model_tau_control = model_data['model_tau_control']
        self.propensity_model = model_data['propensity_model']
        self.feature_names = model_data['feature_names']
        self.is_fitted = model_data['is_fitted']
        logger.info(f"Model loaded from {path}")


class UpliftModelingEngine:
    """Main engine for uplift modeling and treatment recommendations"""

    def __init__(self):
        self.x_learner = XLearner()
        self.feature_columns = [
            'days_since_last_activity',
            'activity_count_30d',
            'activity_count_90d',
            'total_value_30d',
            'total_value_90d',
            'avg_value_per_activity',
            'recency_score',
            'frequency_score',
            'monetary_score',
            'rfm_score',
            'tenure_days',
            'engagement_score',
            'activity_trend',
            'feature_usage_count',
            'session_count_30d',
            'support_tickets_30d',
            'satisfaction_score',
            'payment_failures',
            'account_balance'
        ]

    def train(self, df: pd.DataFrame):
        """
        Train uplift model on normalized dataset.

        Args:
            df: Normalized dataframe with treatment and outcome columns
        """
        logger.info(f"Training uplift model on {len(df)} customers...")

        # Validate data
        self._validate_training_data(df)

        # Prepare features
        X = df[self.feature_columns].fillna(0)
        treatment = df['treatment'].values
        outcome = df['outcome'].values

        # Train X-Learner
        self.x_learner.fit(X, treatment, outcome)

        # Calculate and log performance metrics
        self._log_training_metrics(df, X, treatment, outcome)

    def predict_uplift(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Predict uplift scores for customers.

        Returns:
            DataFrame with uplift scores and customer types
        """
        X = df[self.feature_columns].fillna(0)

        # Get uplift scores
        uplift_scores = self.x_learner.predict_uplift(X)

        # Classify customer types based on uplift
        customer_types = self._classify_customer_types(uplift_scores, df)

        results = pd.DataFrame({
            'customer_id': df['customer_id'],
            'uplift_score': uplift_scores,
            'customer_type': customer_types,
            'churn_prob_with_treatment': self.x_learner.predict_churn_probability(X, treatment_value=1),
            'churn_prob_without_treatment': self.x_learner.predict_churn_probability(X, treatment_value=0)
        })

        return results

    def _classify_customer_types(self, uplift_scores: np.ndarray, df: pd.DataFrame) -> List[str]:
        """
        Classify customers into 4 types:
        - Persuadables: Positive uplift, will respond to treatment
        - Sure Things: Low baseline churn, will stay anyway
        - Lost Causes: High churn, won't respond to treatment
        - Sleeping Dogs: Negative uplift, treatment increases churn
        """
        customer_types = []

        X = df[self.feature_columns].fillna(0)
        baseline_churn_prob = self.x_learner.predict_churn_probability(X, treatment_value=0)

        for i, (uplift, baseline_churn) in enumerate(zip(uplift_scores, baseline_churn_prob)):
            if uplift > 0.1:  # Significant positive uplift
                customer_types.append('Persuadable')
            elif uplift < -0.1:  # Negative uplift - treatment harms
                customer_types.append('Sleeping Dog')
            elif baseline_churn < 0.3:  # Low churn risk anyway
                customer_types.append('Sure Thing')
            else:  # High churn, no uplift
                customer_types.append('Lost Cause')

        return customer_types

    def _validate_training_data(self, df: pd.DataFrame):
        """Validate that training data meets requirements"""
        required_cols = ['treatment', 'outcome'] + self.feature_columns

        # Check required columns
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        # Check treatment balance
        treatment_rate = df['treatment'].mean()
        if treatment_rate < 0.05 or treatment_rate > 0.95:
            logger.warning(f"Treatment rate is {treatment_rate:.2%}, which may be imbalanced")

        # Check sample sizes
        treatment_count = df['treatment'].sum()
        control_count = len(df) - treatment_count

        if treatment_count < 100:
            raise ValueError(f"Treatment group too small: {treatment_count} (need at least 100)")
        if control_count < 100:
            raise ValueError(f"Control group too small: {control_count} (need at least 100)")

        logger.info(f"Data validation passed: {treatment_count} treatment, {control_count} control")

    def _log_training_metrics(self, df: pd.DataFrame, X: pd.DataFrame, treatment: np.ndarray, outcome: np.ndarray):
        """Log training metrics and baseline statistics"""

        # Calculate baseline metrics
        control_churn_rate = outcome[treatment == 0].mean()
        treatment_churn_rate = outcome[treatment == 1].mean()
        baseline_uplift = control_churn_rate - treatment_churn_rate

        logger.info("="*60)
        logger.info("TRAINING METRICS")
        logger.info("="*60)
        logger.info(f"Total customers: {len(df)}")
        logger.info(f"Treatment group: {treatment.sum()} ({treatment.mean():.2%})")
        logger.info(f"Control group: {len(df) - treatment.sum()} ({(1-treatment.mean()):.2%})")
        logger.info(f"Control churn rate: {control_churn_rate:.2%}")
        logger.info(f"Treatment churn rate: {treatment_churn_rate:.2%}")
        logger.info(f"Baseline uplift: {baseline_uplift:.2%}")
        logger.info("="*60)

    def save_model(self, path: str):
        """Save trained model"""
        self.x_learner.save(path)

    def load_model(self, path: str):
        """Load trained model"""
        self.x_learner.load(path)


class InterventionOptimizer:
    """
    Optimizes intervention allocation based on uplift scores and ROI.
    """

    def __init__(self):
        self.intervention_configs = self._load_intervention_configs()

    def _load_intervention_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load intervention configurations for different scenarios"""
        return {
            'discount_10pct': {
                'type': 'discount',
                'cost_pct': 0.10,  # 10% of customer value
                'channel': 'email',
                'message_template': 'Enjoy {amount} off your next purchase',
                'min_clv': 100
            },
            'discount_15pct': {
                'type': 'discount',
                'cost_pct': 0.15,
                'channel': 'in_app',
                'message_template': 'As a valued customer, get {amount} off',
                'min_clv': 500
            },
            'vip_support': {
                'type': 'support_call',
                'cost': 0,  # Internal cost
                'channel': 'phone',
                'message_template': 'Personal account manager will reach out',
                'min_clv': 1000
            },
            'personalized_recommendations': {
                'type': 'content',
                'cost': 0,
                'channel': 'email',
                'message_template': 'Products picked just for you',
                'min_clv': 50
            }
        }

    def recommend_interventions(
        self,
        customer_data: pd.DataFrame,
        uplift_predictions: pd.DataFrame,
        budget: Optional[float] = None,
        min_uplift_threshold: float = 0.1,
        max_interventions: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Recommend optimal interventions for each customer.

        Args:
            customer_data: Customer features including CLV estimates
            uplift_predictions: Predictions from uplift model
            budget: Maximum budget for interventions
            min_uplift_threshold: Minimum uplift score to consider intervention
            max_interventions: Maximum number of customers to target

        Returns:
            DataFrame with recommended interventions per customer
        """
        logger.info("Optimizing intervention allocation...")

        recommendations = []

        for idx, row in uplift_predictions.iterrows():
            customer = customer_data.loc[customer_data['customer_id'] == row['customer_id']].iloc[0]

            # Skip if negative uplift (Sleeping Dogs) or low uplift
            if row['uplift_score'] < min_uplift_threshold:
                continue

            # Skip Sure Things (low churn risk without treatment)
            if row['customer_type'] == 'Sure Thing':
                continue

            # Estimate CLV
            clv = self._estimate_clv(customer)

            # Find best intervention for this customer
            best_intervention = self._select_best_intervention(
                row['uplift_score'],
                clv,
                customer
            )

            if best_intervention:
                recommendations.append({
                    'customer_id': row['customer_id'],
                    'uplift_score': row['uplift_score'],
                    'customer_type': row['customer_type'],
                    'clv_estimate': clv,
                    **best_intervention
                })

        recommendations_df = pd.DataFrame(recommendations)

        if len(recommendations_df) == 0:
            logger.warning("No interventions recommended")
            return recommendations_df

        # Sort by expected value
        recommendations_df = recommendations_df.sort_values('expected_value', ascending=False)

        # Apply budget constraint if specified
        if budget is not None:
            recommendations_df = self._apply_budget_constraint(recommendations_df, budget)

        # Apply max interventions limit
        if max_interventions is not None:
            recommendations_df = recommendations_df.head(max_interventions)

        logger.info(f"Recommended {len(recommendations_df)} interventions")

        return recommendations_df

    def _estimate_clv(self, customer: pd.Series) -> float:
        """Estimate Customer Lifetime Value"""
        # Simple CLV estimation: average monthly value * expected remaining lifetime
        monthly_value = customer['total_value_30d']
        tenure_months = customer['tenure_days'] / 30

        # Estimate remaining lifetime based on engagement
        if customer['engagement_score'] > 70:
            expected_remaining_months = 24
        elif customer['engagement_score'] > 40:
            expected_remaining_months = 12
        else:
            expected_remaining_months = 6

        clv = monthly_value * expected_remaining_months
        return max(clv, 0)

    def _select_best_intervention(
        self,
        uplift_score: float,
        clv: float,
        customer: pd.Series
    ) -> Optional[Dict[str, Any]]:
        """Select best intervention for a customer based on uplift and CLV"""

        best_intervention = None
        best_roi = -np.inf

        for intervention_id, config in self.intervention_configs.items():
            # Check if customer meets minimum CLV requirement
            if clv < config.get('min_clv', 0):
                continue

            # Calculate cost
            if 'cost_pct' in config:
                cost = clv * config['cost_pct']
            else:
                cost = config.get('cost', 0)

            # Calculate expected value
            # Expected value = uplift * CLV - cost
            expected_value = uplift_score * clv - cost

            # Calculate ROI
            if cost > 0:
                roi = (expected_value / cost) * 100
            else:
                roi = expected_value * 100  # If no cost, ROI is just expected value

            # Select intervention with best ROI
            if roi > best_roi and expected_value > 0:
                best_roi = roi
                best_intervention = {
                    'treatment_id': intervention_id,
                    'intervention_type': config['type'],
                    'channel': config['channel'],
                    'message_template': config['message_template'],
                    'cost': cost,
                    'expected_value': expected_value,
                    'roi': roi,
                    'recommended_timing': 'immediate' if uplift_score > 0.3 else 'within_24h'
                }

        return best_intervention

    def _apply_budget_constraint(self, recommendations_df: pd.DataFrame, budget: float) -> pd.DataFrame:
        """Apply budget constraint using greedy approach"""
        total_cost = 0
        selected_indices = []

        for idx, row in recommendations_df.iterrows():
            if total_cost + row['cost'] <= budget:
                selected_indices.append(idx)
                total_cost += row['cost']
            else:
                break

        logger.info(f"Budget constraint applied: ${total_cost:.2f} / ${budget:.2f}")

        return recommendations_df.loc[selected_indices]
