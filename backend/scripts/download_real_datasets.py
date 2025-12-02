"""
Download and prepare real datasets for behavior analysis.

This script downloads actual datasets from public sources:
1. Criteo Uplift Modeling Dataset
2. Hillstrom Email Marketing Dataset
3. IBM Telco Customer Churn Dataset
4. Generates synthetic Financial Services and B2B SaaS datasets

Usage:
    python scripts/download_real_datasets.py
"""

import pandas as pd
import numpy as np
import requests
from pathlib import Path
import zipfile
import io
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Output directory
OUTPUT_DIR = Path("data/real_datasets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)


def download_criteo_dataset():
    """
    Download Criteo Uplift Modeling Dataset

    Note: The full Criteo dataset is very large (25GB+). This function provides
    instructions for manual download or uses a sample if available.
    """
    logger.info("=" * 60)
    logger.info("CRITEO UPLIFT MODELING DATASET")
    logger.info("=" * 60)

    output_path = OUTPUT_DIR / "criteo_uplift.csv"

    logger.info("""
The Criteo Uplift Dataset is available at:
https://ailab.criteo.com/criteo-uplift-prediction-dataset/

Due to its large size (25GB+), please download manually:
1. Visit: https://ailab.criteo.com/criteo-uplift-prediction-dataset/
2. Download the training dataset
3. Extract and save to: data/real_datasets/criteo_uplift.csv

For testing, we'll generate a realistic sample dataset instead.
""")

    # Generate a realistic Criteo-style sample
    logger.info("Generating Criteo-style sample dataset (10,000 records)...")
    from generate_sample_data import generate_criteo_dataset

    df = generate_criteo_dataset(10000)
    df.to_csv(output_path, index=False)

    logger.info(f"✓ Saved Criteo sample to {output_path}")
    logger.info(f"  Records: {len(df):,}")
    logger.info(f"  Treatment rate: {df['treatment'].mean():.2%}")
    logger.info(f"  Conversion rate: {df['conversion'].mean():.2%}\n")

    return df


def download_hillstrom_dataset():
    """
    Download Hillstrom Email Marketing Dataset

    This is from Kevin Hillstrom's MineThatData E-Mail Analytics Challenge.
    """
    logger.info("=" * 60)
    logger.info("HILLSTROM EMAIL MARKETING DATASET")
    logger.info("=" * 60)

    output_path = OUTPUT_DIR / "hillstrom_email.csv"

    # URL for Hillstrom dataset (hosted on GitHub or other public sources)
    url = "https://raw.githubusercontent.com/minethatdata/hillstrom_email_challenge/master/hillstrom.csv"

    try:
        logger.info(f"Downloading from {url}...")

        # Try to download
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            df.to_csv(output_path, index=False)

            logger.info(f"✓ Downloaded Hillstrom dataset to {output_path}")
            logger.info(f"  Records: {len(df):,}")
            logger.info(f"  Columns: {', '.join(df.columns)}\n")

            return df
        else:
            raise Exception(f"Download failed with status {response.status_code}")

    except Exception as e:
        logger.warning(f"Could not download from {url}: {str(e)}")
        logger.info("Generating Hillstrom-style sample dataset instead...")

        from generate_sample_data import generate_hillstrom_dataset
        df = generate_hillstrom_dataset(10000)
        df.to_csv(output_path, index=False)

        logger.info(f"✓ Generated Hillstrom sample to {output_path}")
        logger.info(f"  Records: {len(df):,}\n")

        return df


def download_telco_dataset():
    """
    Download IBM Telco Customer Churn Dataset

    Available from IBM Watson Analytics sample datasets or Kaggle.
    """
    logger.info("=" * 60)
    logger.info("IBM TELCO CUSTOMER CHURN DATASET")
    logger.info("=" * 60)

    output_path = OUTPUT_DIR / "telco_churn.csv"

    # Try multiple sources
    urls = [
        "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv",
        "https://community.ibm.com/community/user/businessanalytics/blogs/steven-macko/2019/07/11/telco-customer-churn-1113"
    ]

    for url in urls:
        try:
            logger.info(f"Trying to download from {url}...")
            response = requests.get(url, timeout=30)

            if response.status_code == 200:
                df = pd.read_csv(io.StringIO(response.text))

                # Process Telco dataset
                # The IBM Telco dataset needs some preprocessing
                if 'Churn' in df.columns:
                    # Convert Churn to binary
                    df['churned'] = (df['Churn'] == 'Yes').astype(int)

                    # Create treatment column (simulate a retention campaign)
                    # Randomly assign 25% to treatment group
                    df['treatment'] = np.random.binomial(1, 0.25, len(df))

                    # Ensure customer_id exists
                    if 'customerID' in df.columns:
                        df['customer_id'] = df['customerID']
                    else:
                        df['customer_id'] = [f'TELCO{i:06d}' for i in range(len(df))]

                df.to_csv(output_path, index=False)

                logger.info(f"✓ Downloaded IBM Telco dataset to {output_path}")
                logger.info(f"  Records: {len(df):,}")
                logger.info(f"  Churn rate: {df['churned'].mean():.2%}\n")

                return df

        except Exception as e:
            logger.warning(f"Failed to download from {url}: {str(e)}")
            continue

    # If all downloads fail, generate synthetic telco dataset
    logger.info("Generating synthetic telco dataset...")
    df = generate_telco_dataset(7043)  # IBM Telco has 7,043 customers
    df.to_csv(output_path, index=False)

    logger.info(f"✓ Generated Telco dataset to {output_path}")
    logger.info(f"  Records: {len(df):,}\n")

    return df


def generate_telco_dataset(n_samples=7043):
    """
    Generate a synthetic telco churn dataset matching IBM Telco structure
    """
    logger.info(f"Generating Telco dataset with {n_samples} samples...")

    # Treatment assignment (25% get retention offer)
    treatment = np.random.binomial(1, 0.25, n_samples)

    data = {
        'customer_id': [f'TELCO{i:06d}' for i in range(n_samples)],
        'treatment': treatment,
    }

    # Demographics
    data['gender'] = np.random.choice(['Male', 'Female'], n_samples)
    data['SeniorCitizen'] = np.random.binomial(1, 0.16, n_samples)  # 16% seniors
    data['Partner'] = np.random.choice(['Yes', 'No'], n_samples, p=[0.48, 0.52])
    data['Dependents'] = np.random.choice(['Yes', 'No'], n_samples, p=[0.30, 0.70])

    # Tenure
    data['tenure'] = np.random.choice(range(1, 73), n_samples)  # 1-72 months

    # Services
    data['PhoneService'] = np.random.choice(['Yes', 'No'], n_samples, p=[0.90, 0.10])
    data['MultipleLines'] = np.random.choice(['Yes', 'No', 'No phone service'], n_samples, p=[0.42, 0.48, 0.10])
    data['InternetService'] = np.random.choice(['DSL', 'Fiber optic', 'No'], n_samples, p=[0.34, 0.44, 0.22])
    data['OnlineSecurity'] = np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.28, 0.50, 0.22])
    data['OnlineBackup'] = np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.34, 0.44, 0.22])
    data['DeviceProtection'] = np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.34, 0.44, 0.22])
    data['TechSupport'] = np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.29, 0.49, 0.22])
    data['StreamingTV'] = np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.38, 0.40, 0.22])
    data['StreamingMovies'] = np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.39, 0.39, 0.22])

    # Contract & Billing
    data['Contract'] = np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples, p=[0.55, 0.21, 0.24])
    data['PaperlessBilling'] = np.random.choice(['Yes', 'No'], n_samples, p=[0.59, 0.41])
    data['PaymentMethod'] = np.random.choice(
        ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'],
        n_samples,
        p=[0.34, 0.15, 0.22, 0.29]
    )

    # Charges
    data['MonthlyCharges'] = np.random.lognormal(4.0, 0.4, n_samples).clip(18, 120)
    data['TotalCharges'] = data['MonthlyCharges'] * data['tenure']

    # Generate churn with treatment effect
    # Base churn probability
    base_churn_prob = 1 / (1 + np.exp(-(
        0.5 +
        -0.015 * data['tenure'] +
        0.8 * (data['Contract'] == 'Month-to-month') +
        0.3 * (data['InternetService'] == 'Fiber optic') +
        0.01 * data['MonthlyCharges'] +
        -0.5 * (data['OnlineSecurity'] == 'Yes') +
        -0.4 * (data['TechSupport'] == 'Yes')
    )))

    # Treatment effect (retention offer reduces churn)
    treatment_effect = -0.6 * treatment

    churn_prob = 1 / (1 + np.exp(-(np.log(base_churn_prob / (1 - base_churn_prob)) + treatment_effect)))
    churned = np.random.binomial(1, churn_prob)

    data['churned'] = churned
    data['Churn'] = ['Yes' if c else 'No' for c in churned]

    df = pd.DataFrame(data)

    logger.info(f"  Treatment rate: {treatment.mean():.2%}")
    logger.info(f"  Churn rate (treatment): {churned[treatment==1].mean():.2%}")
    logger.info(f"  Churn rate (control): {churned[treatment==0].mean():.2%}")
    logger.info(f"  Uplift: {(churned[treatment==0].mean() - churned[treatment==1].mean()):.2%}")

    return df


def generate_financial_dataset(n_samples=10000):
    """
    Generate synthetic Financial Services dataset
    """
    logger.info("=" * 60)
    logger.info("FINANCIAL SERVICES DATASET (Synthetic)")
    logger.info("=" * 60)

    output_path = OUTPUT_DIR / "financial_services.csv"

    from generate_sample_data import generate_financial_dataset as gen_fin
    df = gen_fin(n_samples)
    df.to_csv(output_path, index=False)

    logger.info(f"✓ Generated Financial Services dataset to {output_path}")
    logger.info(f"  Records: {len(df):,}\n")

    return df


def generate_b2b_dataset(n_samples=5000):
    """
    Generate synthetic B2B SaaS dataset
    """
    logger.info("=" * 60)
    logger.info("B2B SAAS DATASET (Synthetic)")
    logger.info("=" * 60)

    output_path = OUTPUT_DIR / "b2b_saas.csv"

    from generate_sample_data import generate_b2b_dataset as gen_b2b
    df = gen_b2b(n_samples)
    df.to_csv(output_path, index=False)

    logger.info(f"✓ Generated B2B SaaS dataset to {output_path}")
    logger.info(f"  Records: {len(df):,}\n")

    return df


def main():
    """Download/generate all datasets"""
    logger.info("\n" + "=" * 60)
    logger.info("DOWNLOADING REAL DATASETS FOR BEHAVIOR ANALYSIS")
    logger.info("=" * 60 + "\n")

    datasets = {}

    # Download/generate each dataset
    datasets['criteo'] = download_criteo_dataset()
    datasets['hillstrom'] = download_hillstrom_dataset()
    datasets['telco'] = download_telco_dataset()
    datasets['financial'] = generate_financial_dataset()
    datasets['b2b'] = generate_b2b_dataset()

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("DOWNLOAD COMPLETE!")
    logger.info("=" * 60)
    logger.info(f"\nDatasets saved to: {OUTPUT_DIR.absolute()}")
    logger.info("\nDataset Summary:")
    logger.info("-" * 60)
    for name, df in datasets.items():
        logger.info(f"  {name.upper():15s} - {len(df):,} records")

    logger.info("\n" + "=" * 60)
    logger.info("NEXT STEPS")
    logger.info("=" * 60)
    logger.info("""
1. Start the backend server:
   cd backend
   python -m uvicorn app.main:app --reload --port 5000

2. Upload datasets via API:
   python scripts/upload_datasets.py

3. Or use the UI:
   cd frontend
   npm run dev

   Navigate to: http://localhost:5173/behavior-analysis

4. Explore the results through the API or UI!
""")


if __name__ == "__main__":
    main()
