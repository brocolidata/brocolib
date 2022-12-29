# Fixtures shared for all utils tests
import pytest
import pandas as pd
from brocolib_utils.utils import gcs
import logging

TEST_BUCKET_NAME = "brocolib_utils-test-bucket"
BUCKET_LOCATION = "EU"
BUCKET_STORAGE_CLASS = "STANDARD"
DEMO_DATA_URL = "https://github.com/Teradata/kylo/blob/master/samples/sample-data/parquet/{file_name}.parquet?raw=true"

@pytest.fixture(scope='session')
def create_test_bucket():
    bucket, bucket_exists = gcs.create_bucket(TEST_BUCKET_NAME)
    msg = f"{bucket.name} already exists" if bucket_exists else f"Created {bucket.name}"
    logging.info(msg)
    yield bucket, bucket_exists
    bucket.delete(force=True)

@pytest.fixture(scope='session')
def populate_bucket(create_test_bucket):
    bucket, bucket_exists = create_test_bucket
    if not bucket_exists:
        for file_number in range(1,4):
            file_name = f"userdata{file_number}"
            url = DEMO_DATA_URL.format(file_name=file_name)
            df = pd.read_parquet(url)
            gcs_url = f"gs://{bucket.name}/test_source/test_table/month={file_number}/{file_name}.parquet"
            df.to_parquet(gcs_url)
            logging.info(f'Loaded {gcs_url}')
    else:
        logging.info('Skipping populate since bucket already exists')
    return bucket