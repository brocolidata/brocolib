import pandas as pd
from .conftest import TEST_BUCKET_NAME, populate_bucket
from brocolib_utils.utils import datalake, gcs
from brocolib_utils import settings
from brocolib_utils.ddm import sources_parser

# def test_no_import_error():
#     from brocolib_utils.datalake import datalake
#     pass


# def test_create_bucket():
#     bucket = datalake.create_bucket(BUCKET_NAME)
#     assert bucket.name == BUCKET_NAME
#     assert bucket.location == BUCKET_LOCATION
#     assert bucket.storage_class == BUCKET_STORAGE_CLASS

# def test_delete_bucket():
#     datalake.delete_bucket(BUCKET_NAME)
#     assert BUCKET_NAME not in datalake.list_buckets()


def test_setup_ok(populate_bucket):
    bucket = populate_bucket
    storage_client = gcs.get_storage_client()
    raw_blobs = storage_client.list_blobs(bucket.name, prefix="test_source/")
    blobs = [blob.name for blob in raw_blobs]
    assert blobs == [
        "test_source/test_table/month=1/userdata1.parquet",
        "test_source/test_table/month=2/userdata2.parquet",
        "test_source/test_table/month=3/userdata3.parquet"
    ]


def test_get_sources(populate_bucket):
    bucket = populate_bucket
    test_source = datalake.get_source(
        gcp_project=settings.DATALAKE_PROJECT, 
        datalake_bucket=bucket.name, 
        source_name="test_source"
    )
    assert test_source == {
        'test_table': 'gs://brocolib_utils-test-bucket/test_source/test_table/'
    }    



def test_get_all_columns_for_tables(populate_bucket):
    source_columns = sources_parser.get_source_columns(
        source_name="test_source",
        table_name="test_table",
        datalake_bucket=TEST_BUCKET_NAME
    )

    assert source_columns == [
        {"name": "registration_dttm", "type": "TIMESTAMP"},
        {"name": "id", "type": "FLOAT"},
        {"name": "first_name", "type": "STRING"},
        {"name": "last_name", "type": "STRING"},
        {"name": "email", "type": "STRING"},
        {"name": "gender", "type": "STRING"},
        {"name": "ip_address", "type": "STRING"},
        {"name": "cc", "type": "STRING"},
        {"name": "country", "type": "STRING"},
        {"name": "birthdate", "type": "STRING"},
        {"name": "salary", "type": "FLOAT"},
        {"name": "title", "type": "STRING"},
        {"name": "comments", "type": "STRING"},
        {"name": "month", "type": "STRING"},
    ]

