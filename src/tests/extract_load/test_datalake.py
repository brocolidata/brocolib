# contents of test_app.py, a simple test for our API retrieval
from datetime import datetime
import pytest
import pandas as pd
from requests import get
from extract_load.brocolib_extract_load import datalake

DEFAULT_BUCKET = "test-bucket"
DEFAULT_FILE = "test_file"
DEFAULT_SUBFOLDERS = "macro"
DEFAULT_TABLE_FOLDER = "table_folder"
DEFAULT_BLOB_NAME = f"{DEFAULT_SUBFOLDERS}/{DEFAULT_TABLE_FOLDER}/{DEFAULT_FILE}"
DEFAULT_DBT_TOPIC = "test_dbt_topic"
DEFAULT_GCP_PROJECT = "default-gcp-project"
DEFAULT_PARTITION_KEYS = {"year":"","month":""}

## -----| Fixtures |-----

# custom class to be the mock pandas.DataFrame.to_*() methods
class MockPandas:
    @staticmethod
    def json():
        return None


# fixture monkeypatch
@pytest.fixture
def mock_pandas(monkeypatch):
    """Requests.get() mocked to return {'mock_key':'mock_response'}."""

    def mock_get(*args, **kwargs):
        return MockPandas()

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_get)
    monkeypatch.setattr(pd.DataFrame, "to_parquet", mock_get)


@pytest.fixture(params=["get_dummy_df", "get_empty_df"])
def matrix_df(request):
    df_fixture = request.getfixturevalue(request.param)
    return df_fixture

@pytest.fixture(params=["csv", "parquet"])
def matrix_format(request):
    return request.param


## -----| Tests |-----

def test_dataframe_to_bucket(mock_pandas, matrix_df, matrix_format):
    result = datalake.dataframe_to_bucket(
        dataframe=matrix_df,
        bucket_name=DEFAULT_BUCKET,
        blob_name=DEFAULT_BLOB_NAME,
        file_type=matrix_format
    )
    assert result == f"gs://{DEFAULT_BUCKET}/{DEFAULT_BLOB_NAME}.{matrix_format}"

def test_external_table(mock_pandas):
    external_table = datalake.ExternalTable(
        bucket_name=DEFAULT_BUCKET,
        partition_keys=DEFAULT_PARTITION_KEYS,
        bucket_file=DEFAULT_FILE,
        bucket_table_directory=DEFAULT_TABLE_FOLDER,
        bucket_directory=DEFAULT_SUBFOLDERS,
        dbt_topic=DEFAULT_DBT_TOPIC,
        gcp_project=DEFAULT_GCP_PROJECT,
    )
    now = datetime.now()
    path_prefix = f'{DEFAULT_SUBFOLDERS}/{DEFAULT_TABLE_FOLDER}'
    path_partitions = f'year={now.year}/month={now.month}'
    assert external_table.add_partition_keys(path_prefix) == f'{path_prefix}/{path_partitions}'
    assert external_table.format_filename() == f'{path_prefix}/{path_partitions}/{DEFAULT_FILE}_{str(now.day)}'
