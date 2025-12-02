"""
Automatically upload downloaded datasets to the behavior analysis system.

This script uploads all datasets from data/real_datasets/ to the backend API.

Prerequisites:
1. Backend server must be running (http://localhost:5000)
2. You must have a valid user account
3. Datasets must be in data/real_datasets/

Usage:
    python scripts/upload_datasets.py --email your@email.com --password yourpassword
"""

import requests
import argparse
from pathlib import Path
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_BASE = "http://localhost:5000/api/v1"
DATASETS_DIR = Path("data/real_datasets")


def login(email: str, password: str) -> str:
    """Login and get auth token"""
    logger.info(f"Logging in as {email}...")

    try:
        response = requests.post(
            f"{API_BASE}/auth/login",
            data={"username": email, "password": password}
        )

        if response.status_code == 200:
            token = response.json()["access_token"]
            logger.info("✓ Login successful")
            return token
        else:
            logger.error(f"Login failed: {response.text}")
            raise Exception(f"Login failed with status {response.status_code}")

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise


def upload_dataset(file_path: Path, dataset_name: str, dataset_type: str, token: str):
    """Upload a single dataset"""
    logger.info(f"Uploading {dataset_name} ({dataset_type})...")

    if not file_path.exists():
        logger.warning(f"File not found: {file_path}")
        return None

    headers = {"Authorization": f"Bearer {token}"}

    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f, 'text/csv')}
            data = {
                'dataset_name': dataset_name,
                'dataset_type': dataset_type,
                'auto_train': 'true'
            }

            response = requests.post(
                f"{API_BASE}/behavior/upload-data",
                files=files,
                data=data,
                headers=headers
            )

        if response.status_code == 200:
            result = response.json()
            dataset_id = result['dataset_id']
            logger.info(f"✓ Upload successful - Dataset ID: {dataset_id}")
            logger.info(f"  Status: {result['status']}")
            return dataset_id
        else:
            logger.error(f"Upload failed: {response.text}")
            return None

    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return None


def check_dataset_status(dataset_id: str, token: str, wait_for_completion: bool = False):
    """Check processing status of a dataset"""
    headers = {"Authorization": f"Bearer {token}"}

    while True:
        try:
            response = requests.get(
                f"{API_BASE}/behavior/data/status/{dataset_id}",
                headers=headers
            )

            if response.status_code == 200:
                status_data = response.json()
                status = status_data['status']

                logger.info(f"  Status: {status}")

                if status == 'completed':
                    logger.info(f"  ✓ Processing complete!")
                    logger.info(f"    Total records: {status_data.get('total_records', 'N/A'):,}")
                    logger.info(f"    Treatment: {status_data.get('treatment_count', 'N/A'):,}")
                    logger.info(f"    Control: {status_data.get('control_count', 'N/A'):,}")
                    return True
                elif status == 'failed':
                    logger.error(f"  ✗ Processing failed!")
                    return False
                elif wait_for_completion:
                    logger.info(f"  Processing... waiting 5 seconds")
                    time.sleep(5)
                else:
                    return None
            else:
                logger.error(f"Status check failed: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Status check error: {str(e)}")
            return False

        if not wait_for_completion:
            break


def main():
    parser = argparse.ArgumentParser(description='Upload datasets to behavior analysis system')
    parser.add_argument('--email', required=True, help='User email')
    parser.add_argument('--password', required=True, help='User password')
    parser.add_argument('--wait', action='store_true', help='Wait for processing to complete')
    parser.add_argument('--datasets', nargs='+', choices=['criteo', 'hillstrom', 'telco', 'financial', 'b2b'],
                        help='Specific datasets to upload (default: all)')

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("UPLOADING DATASETS TO BEHAVIOR ANALYSIS SYSTEM")
    logger.info("=" * 60)

    # Login
    try:
        token = login(args.email, args.password)
    except Exception as e:
        logger.error("Failed to login. Exiting.")
        return

    # Define datasets to upload
    datasets_to_upload = {
        'criteo': {
            'file': DATASETS_DIR / 'criteo_uplift.csv',
            'name': 'Criteo Uplift Dataset',
            'type': 'criteo'
        },
        'hillstrom': {
            'file': DATASETS_DIR / 'hillstrom_email.csv',
            'name': 'Hillstrom Email Marketing Campaign',
            'type': 'hillstrom'
        },
        'telco': {
            'file': DATASETS_DIR / 'telco_churn.csv',
            'name': 'IBM Telco Customer Churn',
            'type': 'telco'
        },
        'financial': {
            'file': DATASETS_DIR / 'financial_services.csv',
            'name': 'Financial Services Customer Data',
            'type': 'financial'
        },
        'b2b': {
            'file': DATASETS_DIR / 'b2b_saas.csv',
            'name': 'B2B SaaS Customer Data',
            'type': 'b2b'
        }
    }

    # Filter datasets if specified
    if args.datasets:
        datasets_to_upload = {k: v for k, v in datasets_to_upload.items() if k in args.datasets}

    # Upload each dataset
    uploaded_ids = {}

    logger.info(f"\nUploading {len(datasets_to_upload)} dataset(s)...\n")

    for key, dataset_info in datasets_to_upload.items():
        logger.info("-" * 60)
        dataset_id = upload_dataset(
            dataset_info['file'],
            dataset_info['name'],
            dataset_info['type'],
            token
        )

        if dataset_id:
            uploaded_ids[key] = dataset_id

            # Check initial status
            check_dataset_status(dataset_id, token, wait_for_completion=False)

        logger.info("")

    # Wait for completion if requested
    if args.wait and uploaded_ids:
        logger.info("=" * 60)
        logger.info("WAITING FOR PROCESSING TO COMPLETE")
        logger.info("=" * 60)

        for key, dataset_id in uploaded_ids.items():
            logger.info(f"\nChecking {datasets_to_upload[key]['name']}...")
            check_dataset_status(dataset_id, token, wait_for_completion=True)

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("UPLOAD SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Successfully uploaded: {len(uploaded_ids)}/{len(datasets_to_upload)} datasets")

    if uploaded_ids:
        logger.info("\nDataset IDs:")
        for key, dataset_id in uploaded_ids.items():
            logger.info(f"  {key:12s} - {dataset_id}")

    logger.info("\n" + "=" * 60)
    logger.info("NEXT STEPS")
    logger.info("=" * 60)
    logger.info("""
1. Check dataset status:
   curl -X GET "http://localhost:5000/api/v1/behavior/data/status/<dataset_id>" \\
     -H "Authorization: Bearer <token>"

2. View dataset statistics:
   curl -X GET "http://localhost:5000/api/v1/behavior/datasets/<dataset_id>/stats" \\
     -H "Authorization: Bearer <token>"

3. Get customer behavior analysis:
   curl -X GET "http://localhost:5000/api/v1/behavior/customers/<customer_id>/behavior?dataset_id=<dataset_id>" \\
     -H "Authorization: Bearer <token>"

4. Or explore via the UI:
   http://localhost:5173/behavior-analysis
""")


if __name__ == "__main__":
    main()
