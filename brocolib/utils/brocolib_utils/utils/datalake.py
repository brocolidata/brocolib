import re
import pandas as pd
from google.cloud import storage
from pandas_gbq.schema import generate_bq_schema
from brocolib_utils import credentials, settings
from . import gcs


def get_storage_client(gcp_project):
    return storage.Client(project=gcp_project)


def get_gsutil_uri(bucket: str, blob: str) -> str:
    """Construct a gsutil uri

    Args:
        bucket (str): Google Cloud Storage bucket name
        blob (str): Suffix of the gsutil uri

    Returns:
        str: The gsutil uri
    """
    return f"gs://{bucket}/{blob}"


def add_to_source_list(
    client: storage.client.Client, 
    datalake_bucket: str, 
    prefix: str = "", 
    sources_dict: dict = {}
):
    """_summary_

    Args:
        client (storage.client.Client): Storage client
        datalake_bucket (str): Google Cloud Storage bucket name
        prefix (str, optional): gsutil uri prefix. Defaults to "".
        sources_dict (dict, optional): dict containing the dbt sources. Defaults to {}.

    Returns:
        _type_: _description_
    """
    result = client.list_blobs(
        bucket_or_name=datalake_bucket,
        prefix=prefix,
        delimiter='/'
    )
    FILE_EXTENSION_PATTERN = r"[\d\D]*\.parquet"
    for element in result:
        if re.match(FILE_EXTENSION_PATTERN, element.name.replace(prefix, "")):
            table_name = prefix.split('/')[-2]  
            sources_dict[table_name] = prefix
            return sources_dict
        pass
    HIVE_PARTITIONING_PATTERN = r"[\d\D]*\=[\d\D]*"
    for element in result.prefixes:
        if re.match(HIVE_PARTITIONING_PATTERN, element.replace(prefix, "")):
            table_name = prefix.split('/')[-2]
            sources_dict[table_name] = prefix
        else:
            add_to_source_list(
                client=client,
                datalake_bucket=datalake_bucket,
                prefix=element,
                sources_dict=sources_dict
            )
    return sources_dict


def get_raw_source(
    gcp_project: str, 
    datalake_bucket: str, 
    source_name: str
) -> dict:
    """_summary_

    Args:
        gcp_project (str): _description_
        datalake_bucket (str): _description_
        first_partition_key (str): _description_

    Returns:
        dict: _description_
    """
    client = gcs.get_storage_client(gcp_project)
    source_dict=add_to_source_list(
        client=client,
        datalake_bucket=datalake_bucket,
        prefix=source_name
    )
    return source_dict

def get_source(
    source_name: str,
    gcp_project: str = None, 
    datalake_bucket: str = None
):
    gcp_project = gcp_project or settings.DATALAKE_PROJECT
    datalake_bucket = datalake_bucket or settings.DATALAKE_BUCKET
    raw_source_dict = get_raw_source(
        gcp_project=gcp_project, 
        datalake_bucket=datalake_bucket, 
        source_name=f"{source_name}/"
    )
    source_dict = {
        table:get_gsutil_uri(datalake_bucket, blob) for table, blob in raw_source_dict.items()
    }
    return source_dict


def generate_bigquery_schema_from_df(df: pd.DataFrame) -> list:
    raw_schema = generate_bq_schema(df)
    return raw_schema["fields"]