# contents of test_app.py, a simple test for our API retrieval
import pytest
import pandas as pd
from requests import get
from extract_load.brocolib_extract_load import datalake

DEFAULT_BUCKET = "test-bucket"
DEFAULT_BLOB_NAME = "folder/subfolder/file"

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