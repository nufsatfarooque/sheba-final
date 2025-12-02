"""
Generate sample datasets for testing the behavior analysis feature.
Creates synthetic data matching Criteo, Hillstrom, Financial, and B2B formats.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

OUTPUT_DIR = Path("data/sample_datasets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_criteo_dataset(n_samples=10000):
    """Generate Criteo-style dataset"""
    print(f"Generating Criteo dataset with {n_samples} samples...")

    # Treatment assignment (30% treatment)
    treatment = np.random.binomial(1, 0.3, n_samples)

    # Generate features (f0-f11)
    data = {
        'treatment': treatment,
        'exposure': treatment,  # Exposed = treated
    }

    # f0: Days since last activity (recency proxy)
    data['f0'] = np.random.exponential(30, n_samples).clip(0, 365)

    # f1: Tenure days
    data['f1'] = np.random.gamma(2, 50, n_samples).clip(7, 1095)

    # f2: Engagement score (0-100)
    data['f2'] = np.random.beta(5, 2, n_samples) * 100

    # f3: Activity trend (-1 to 1)
    data['f3'] = np.random.normal(0, 0.3, n_samples).clip(-1, 1)

    # f4: Activity count 30d
    data['f4'] = np.random.poisson(5, n_samples).clip(0, 100)

    # f5: Activity count 90d
    data['f5'] = data['f4'] * np.random.uniform(2.5, 3.5, n_samples)

    # f6: Feature usage count
    data['f6'] = np.random.poisson(3, n_samples).clip(0, 20)

    # f7: Session count
    data['f7'] = data['f4'] * np.random.uniform(1.5, 2.5, n_samples)

    # f8: Total value 30d
    data['f8'] = np.random.lognormal(4, 1.5, n_samples).clip(0, 10000)

    # f9: Total value 90d
    data['f9'] = data['f8'] * np.random.uniform(2.5, 3.5, n_samples)

    # f10: Avg value per activity
    data['f10'] = data['f8'] / (data['f4'] + 1)

    # f11: Account balance
    data['f11'] = np.random.lognormal(5, 2, n_samples).clip(0, 50000)

    # Generate outcomes with treatment effect
    # Base churn probability
    base_churn_prob = 1 / (1 + np.exp(-(
        -2.0 +
        0.02 * data['f0'] +       # Higher recency = more churn
        -0.1 * data['f2'] / 10 +  # Higher engagement = less churn
        -0.05 * data['f4']        # Higher activity = less churn
    )))

    # Treatment effect (reduces churn by ~12%)
    treatment_effect = -0.5 * treatment

    # Final churn probability
    churn_prob = 1 / (1 + np.exp(-(np.log(base_churn_prob / (1 - base_churn_prob)) + treatment_effect)))

    # Outcome: 0 = conversion (retained), 1 = no conversion (churned)
    conversion = 1 - np.random.binomial(1, churn_prob)
    visit = (conversion | np.random.binomial(1, 0.3, n_samples)).astype(int)

    data['visit'] = visit
    data['conversion'] = conversion

    df = pd.DataFrame(data)

    # Save
    output_path = OUTPUT_DIR / "criteo_sample.csv"
    df.to_csv(output_path, index=False)
    print(f"✓ Saved Criteo dataset to {output_path}")
    print(f"  Treatment rate: {treatment.mean():.2%}")
    print(f"  Conversion rate (treatment): {conversion[treatment==1].mean():.2%}")
    print(f"  Conversion rate (control): {conversion[treatment==0].mean():.2%}")
    print(f"  Uplift: {(conversion[treatment==0].mean() - conversion[treatment==1].mean()):.2%}\n")

    return df


def generate_hillstrom_dataset(n_samples=10000):
    """Generate Hillstrom-style email marketing dataset"""
    print(f"Generating Hillstrom dataset with {n_samples} samples...")

    # Treatment groups: 1/3 control, 1/3 mens, 1/3 womens
    treatment_group = np.random.choice([0, 1, 2], n_samples)
    mens = (treatment_group == 1).astype(int)
    womens = (treatment_group == 2).astype(int)

    data = {
        'mens': mens,
        'womens': womens,
    }

    # Recency: Months since last purchase
    data['recency'] = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], n_samples, p=[0.15, 0.12, 0.10, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.04, 0.10, 0.10])

    # History: Total spend in past 12 months
    data['history'] = np.random.lognormal(5, 1.2, n_samples).clip(10, 5000)

    # Zip code
    data['zip_code'] = np.random.choice(['Rural', 'Suburban', 'Urban'], n_samples, p=[0.2, 0.5, 0.3])

    # Newbie: 0 = returning, 1 = new
    data['newbie'] = np.random.binomial(1, 0.2, n_samples)

    # Channel
    data['channel'] = np.random.choice(['Phone', 'Web', 'Multichannel'], n_samples, p=[0.2, 0.5, 0.3])

    # Generate outcomes with treatment effect
    # Base conversion probability
    base_conv_prob = 1 / (1 + np.exp(-(
        -3.0 +
        -0.15 * data['recency'] +              # Recent buyers convert more
        0.0003 * data['history'] +             # High spenders convert more
        0.5 * (data['channel'] == 'Multichannel') +
        -0.8 * data['newbie']                  # New customers convert less
    )))

    # Treatment effect for mens/womens email
    treatment_effect = 0.8 * mens + 0.6 * womens

    # Final conversion probability
    conv_prob = 1 / (1 + np.exp(-(np.log(base_conv_prob / (1 - base_conv_prob)) + treatment_effect)))

    conversion = np.random.binomial(1, conv_prob)
    visit = (conversion | np.random.binomial(1, 0.15, n_samples)).astype(int)

    # Spend for converters
    spend = np.where(
        conversion == 1,
        np.random.lognormal(3.5, 0.8, n_samples).clip(10, 1000),
        0
    )

    data['visit'] = visit
    data['conversion'] = conversion
    data['spend'] = spend

    df = pd.DataFrame(data)

    # Save
    output_path = OUTPUT_DIR / "hillstrom_sample.csv"
    df.to_csv(output_path, index=False)
    print(f"✓ Saved Hillstrom dataset to {output_path}")
    print(f"  Conversion rate (control): {conversion[treatment_group==0].mean():.2%}")
    print(f"  Conversion rate (mens): {conversion[treatment_group==1].mean():.2%}")
    print(f"  Conversion rate (womens): {conversion[treatment_group==2].mean():.2%}\n")

    return df


def generate_financial_dataset(n_samples=10000):
    """Generate Financial Services dataset"""
    print(f"Generating Financial Services dataset with {n_samples} samples...")

    # Treatment assignment (25% treatment)
    treatment = np.random.binomial(1, 0.25, n_samples)

    data = {
        'customer_id': [f'CUST{i:06d}' for i in range(n_samples)],
        'treatment': treatment,
    }

    # Demographics
    data['age'] = np.random.normal(45, 15, n_samples).clip(18, 85).astype(int)
    data['gender'] = np.random.choice(['M', 'F'], n_samples)

    # Account info
    data['tenure_months'] = np.random.gamma(3, 10, n_samples).clip(1, 300).astype(int)
    data['account_balance'] = np.random.lognormal(7, 2, n_samples).clip(0, 1000000)

    # Transaction metrics
    data['transaction_count_30d'] = np.random.poisson(8, n_samples).clip(0, 100)
    data['transaction_count_90d'] = data['transaction_count_30d'] * np.random.uniform(2.5, 3.5, n_samples)
    data['avg_transaction_value'] = np.random.lognormal(4, 1, n_samples).clip(10, 5000)

    # Engagement
    data['last_login_days'] = np.random.exponential(15, n_samples).clip(0, 365).astype(int)
    data['products_owned'] = np.random.choice([1, 2, 3, 4, 5], n_samples, p=[0.3, 0.3, 0.2, 0.15, 0.05])
    data['mobile_banking_logins'] = np.random.poisson(12, n_samples).clip(0, 200)

    # Support
    data['support_tickets_90d'] = np.random.choice([0, 1, 2, 3, 4, 5], n_samples, p=[0.5, 0.25, 0.12, 0.08, 0.03, 0.02])

    # Risk indicators
    data['payment_failures'] = np.random.choice([0, 1, 2, 3], n_samples, p=[0.8, 0.12, 0.05, 0.03])
    data['credit_score'] = np.random.normal(700, 80, n_samples).clip(300, 850).astype(int)

    # Satisfaction
    data['satisfaction_score'] = np.random.beta(6, 2, n_samples) * 100

    # Generate churn with treatment effect
    base_churn_prob = 1 / (1 + np.exp(-(
        -1.5 +
        0.01 * data['last_login_days'] +
        -0.05 * data['transaction_count_30d'] +
        -0.0001 * data['account_balance'] +
        0.2 * data['payment_failures'] +
        0.15 * data['support_tickets_90d'] +
        -0.01 * data['satisfaction_score']
    )))

    # Treatment effect (retention campaign)
    treatment_effect = -0.7 * treatment

    churn_prob = 1 / (1 + np.exp(-(np.log(base_churn_prob / (1 - base_churn_prob)) + treatment_effect)))
    churned = np.random.binomial(1, churn_prob)

    data['churned'] = churned

    df = pd.DataFrame(data)

    # Save
    output_path = OUTPUT_DIR / "financial_sample.csv"
    df.to_csv(output_path, index=False)
    print(f"✓ Saved Financial Services dataset to {output_path}")
    print(f"  Treatment rate: {treatment.mean():.2%}")
    print(f"  Churn rate (treatment): {churned[treatment==1].mean():.2%}")
    print(f"  Churn rate (control): {churned[treatment==0].mean():.2%}")
    print(f"  Uplift: {(churned[treatment==0].mean() - churned[treatment==1].mean()):.2%}\n")

    return df


def generate_b2b_dataset(n_samples=5000):
    """Generate B2B SaaS dataset"""
    print(f"Generating B2B SaaS dataset with {n_samples} samples...")

    # Treatment assignment (20% treatment - retention calls)
    treatment = np.random.binomial(1, 0.2, n_samples)

    data = {
        'customer_id': [f'B2B{i:05d}' for i in range(n_samples)],
        'treatment': treatment,
    }

    # Contract info
    data['contract_value_per_month'] = np.random.choice(
        [99, 199, 499, 999, 1999, 4999],
        n_samples,
        p=[0.3, 0.25, 0.2, 0.15, 0.07, 0.03]
    )
    data['contract_duration_months'] = np.random.gamma(2, 6, n_samples).clip(1, 60).astype(int)

    # Usage metrics
    data['feature_usage_count'] = np.random.poisson(25, n_samples).clip(0, 500)
    data['days_since_last_login'] = np.random.exponential(7, n_samples).clip(0, 180).astype(int)
    data['api_calls_30d'] = np.random.lognormal(5, 2, n_samples).clip(0, 100000).astype(int)

    # Team metrics
    data['seats_purchased'] = np.random.choice([5, 10, 25, 50, 100, 250], n_samples, p=[0.4, 0.25, 0.15, 0.1, 0.07, 0.03])
    data['seats_active'] = (data['seats_purchased'] * np.random.uniform(0.4, 1.0, n_samples)).astype(int)

    # Support
    data['support_tickets'] = np.random.choice([0, 1, 2, 3, 4, 5, 6], n_samples, p=[0.3, 0.25, 0.2, 0.12, 0.07, 0.04, 0.02])
    data['csat_score'] = np.random.beta(7, 2, n_samples) * 100

    # Metadata
    data['industry'] = np.random.choice(['Technology', 'Finance', 'Healthcare', 'Retail', 'Other'], n_samples)
    data['company_size'] = np.random.choice(['1-10', '11-50', '51-200', '201-1000', '1000+'], n_samples, p=[0.2, 0.3, 0.25, 0.15, 0.1])

    # Onboarding
    data['integrations_enabled'] = np.random.poisson(2, n_samples).clip(0, 20)
    data['onboarding_completed'] = np.random.binomial(1, 0.75, n_samples)

    # Generate churn with treatment effect
    seat_utilization = data['seats_active'] / data['seats_purchased']

    base_churn_prob = 1 / (1 + np.exp(-(
        -2.0 +
        0.015 * data['days_since_last_login'] +
        -0.002 * data['feature_usage_count'] +
        0.2 * data['support_tickets'] +
        -0.01 * data['csat_score'] +
        -1.5 * seat_utilization +
        -0.8 * data['onboarding_completed']
    )))

    # Treatment effect (retention call)
    treatment_effect = -0.9 * treatment

    churn_prob = 1 / (1 + np.exp(-(np.log(base_churn_prob / (1 - base_churn_prob)) + treatment_effect)))
    churned = np.random.binomial(1, churn_prob)

    data['churned'] = churned

    df = pd.DataFrame(data)

    # Save
    output_path = OUTPUT_DIR / "b2b_sample.csv"
    df.to_csv(output_path, index=False)
    print(f"✓ Saved B2B SaaS dataset to {output_path}")
    print(f"  Treatment rate: {treatment.mean():.2%}")
    print(f"  Churn rate (treatment): {churned[treatment==1].mean():.2%}")
    print(f"  Churn rate (control): {churned[treatment==0].mean():.2%}")
    print(f"  Uplift: {(churned[treatment==0].mean() - churned[treatment==1].mean()):.2%}\n")

    return df


if __name__ == "__main__":
    print("=" * 60)
    print("GENERATING SAMPLE DATASETS FOR BEHAVIOR ANALYSIS")
    print("=" * 60 + "\n")

    # Generate all datasets
    criteo_df = generate_criteo_dataset(10000)
    hillstrom_df = generate_hillstrom_dataset(10000)
    financial_df = generate_financial_dataset(10000)
    b2b_df = generate_b2b_dataset(5000)

    print("=" * 60)
    print("ALL DATASETS GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nDatasets saved to: {OUTPUT_DIR.absolute()}")
    print("\nNext steps:")
    print("1. Start the backend server")
    print("2. Upload datasets via API or UI")
    print("3. Explore behavior analysis results\n")
