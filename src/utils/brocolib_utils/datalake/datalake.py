import pandas as pd
from google.cloud import storage
from pandas_gbq.schema import generate_bq_schema
from brocolib_utils.settings import _TYPE_ALIASES

def get_storage_client(gcp_project) -> storage.client.Client:
    return storage.Client(project=gcp_project)


def get_raw_sources(
    gcp_project: str, 
    datalake_bucket: str, 
) -> dict:
    """_summary_

    Args:
        gcp_project (str): _description_
        datalake_bucket (str): _description_
        first_partition_key (str): _description_

    Returns:
        dict: _description_
    """
    client = get_storage_client(gcp_project)
    sources_dict=add_to_source_list(
        client=client,
        datalake_bucket=datalake_bucket,
    )
    return sources_dict


def add_to_source_list(
    client: storage.client.Client,  
    datalake_bucket: str, 
    prefix: str = "", 
    sources_dict: dict = {}
) -> dict:
    """Recursive function that traverse a Google Cloud Storage bucket tree
    and return a dict of source:root dict, the root dict containing
    root gsutil uri prefix:parquet file gsutil uri prefix

    Args:
        client (storage.client.Client): Google Cloud Storage client.
        datalake_bucket (str): Google Cloud Storage bucket name.
        prefix (str, optional): gsutil uri prefix. Defaults to "". Defaults to "".
        sources_dict (dict, optional): dict containing sources. Defaults to {}.

    Returns:
        dict: A dict of source:root dict, the root dict containing root gsutil uri prefix:parquet file gsutil uri prefix 
    """
    result = client.list_blobs(
        bucket_or_name=datalake_bucket,
        prefix=prefix,
        delimiter='/'
    )
    for element in result:
        pass
    
    for element in result.prefixes:
        if "=" in element.replace(prefix, ""):
            table_name = prefix.split('/')[1]
            source_name = prefix.split('/')[0]
            if source_name in sources_dict:
                if table_name in sources_dict[source_name]:
                    sources_dict[source_name][table_name] = prefix
                else:
                    sources_dict[source_name][table_name] = {}
            else:
                sources_dict[source_name] = {}
        else:
            add_to_source_list(
                client=client,
                datalake_bucket=datalake_bucket,
                prefix=element, 
                sources_dict=sources_dict
            )
    return sources_dict


def generate_schema_from_df(df: pd.DataFrame) -> list:
    schema = generate_bq_schema(df)
    columns_list = []
    for kpi in schema["fields"]:
        data_type = kpi["type"]
        if data_type in _TYPE_ALIASES:
            data_type = _TYPE_ALIASES[data_type]
        columns_list.append(
            {"name":kpi["name"], "data_type":data_type}
        )
    return columns_list


# -----| NEW CODE |-----
def get_mapping_parquet_root(
    client: storage.client.Client, 
    datalake_bucket: str, 
    prefix: str = "",
    dc_elements: dict = {},
    file_type: str = "parquet"
) -> dict:
    """Get a map of prefixes:list of files uris for a
    determined external table gsutil uri prefix

    Args:
        client (storage.client.Client): Google Cloud Storage client
        datalake_bucket (str): Google Cloud Storage bucket name
        prefix (str, optional): gsutil uri prefix. Defaults to "".
        dc_elements (dict, optional): mapping dict. Defaults to {}.
        file_type (str, optional): Type of file in Google Cloud Storage. Defaults to "parquet".

    Returns:
        dict: Map of prefixes:list of files uris
    """
    result = client.list_blobs(
        bucket_or_name=datalake_bucket,
        prefix=prefix,
        delimiter='/'
    )
    for element in result:
        dc_elements[prefix].append(element.name)
    
    for element in result.prefixes:
        if not element.endswith(f".{file_type}"):
            dc_elements[element] = []
            get_mapping_parquet_root(
                client=client,
                datalake_bucket=datalake_bucket,
                prefix=element, 
                dc_elements=dc_elements
            )

    return {k:v for k,v in dc_elements.items() if v != []}


def get_storage_client(gcp_project: str) -> storage.client.Client:
    return storage.Client(project=gcp_project)


def add_to_source_list(
    client: storage.client.Client, 
    datalake_bucket: str, 
    first_partition_key: str,
    prefix: str = "", 
    sources_dict: dict = {}
):
    """_summary_

    Args:
        client (storage.client.Client): Storage client
        datalake_bucket (str): Google Cloud Storage bucket name
        first_partition_key (str): First partition key in the gsutil uri.
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
    for element in result:
        pass
    
    for element in result.prefixes:
        if element.replace(prefix, "").startswith(f"{first_partition_key}="):
            table_name = table_name = prefix.split('/')[-2]
            sources_dict[table_name] = prefix
        else:
            add_to_source_list(
                client=client,
                datalake_bucket=datalake_bucket,
                first_partition_key=first_partition_key,
                prefix=element, 
                sources_dict=sources_dict
            )
    return sources_dict


def get_raw_sources(
    gcp_project: str, 
    datalake_bucket: str, 
    first_partition_key: str
) -> dict:
    """_summary_

    Args:
        gcp_project (str): _description_
        datalake_bucket (str): _description_
        first_partition_key (str): _description_

    Returns:
        dict: _description_
    """
    client = get_storage_client(gcp_project)
    sources_dict=add_to_source_list(
        client=client,
        datalake_bucket=datalake_bucket,
        first_partition_key=first_partition_key
    )
    print(sources_dict)
    return sources_dict


def get_gsutil_uri(bucket: str, blob: str) -> str:
    """Construct a gsutil uri

    Args:
        bucket (str): Google Cloud Storage bucket name
        blob (str): Suffix of the gsutil uri

    Returns:
        str: The gsutil uri
    """
    return f"gs://{bucket}/{blob}"


def get_sources(gcp_project, datalake_bucket, first_partition_key):
    raw_sources_dict = get_raw_sources(gcp_project, datalake_bucket, first_partition_key)
    sources_dict = {
        table:get_gsutil_uri(datalake_bucket, blob) for table, blob in raw_sources_dict.items()
    }
    return sources_dict


def get_overall_df(
    bucket: str,
    prefix: str
) -> pd.DataFrame:
    uri = get_gsutil_uri(bucket, prefix)
    return pd.read_parquet(uri)


def generate_bigquery_schema_from_df(df: pd.DataFrame) -> dict:
    return generate_bq_schema(df)


def generate_pandas_schema(df: pd.DataFrame) -> dict:
    SCHEMA_MAPPING = {
        'any': 'categorical',
        'boolean': 'bool',
        'datetime': 'datetime64[ns]',
        'duration': 'timedelta64[ns]',
        'integer': 'int64',
        'number': 'float64',
        'str': 'object'
    }
    schema = build_table_schema(df)
    return {d["name"]:SCHEMA_MAPPING[d["type"]] for d in schema["fields"]}


def generate_root_schema(
    bucket: str, 
    prefix: str,
    example_uri: str
) -> dict:
    
    df = get_overall_df(
        bucket=bucket,
        prefix=prefix
    )
    clean_columns, _ = remove_partition_keys(df.columns, example_uri)
    df[clean_columns]
    return generate_pandas_schema(df)


def apply_schema_to_df(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    return df.astype(schema)


def diagnose_external_table(gcp_project: str, bucket: str, prefix: str):
    table_mapping = get_mapping_parquet_root(
        client=get_storage_client(gcp_project), 
        datalake_bucket=bucket, 
        prefix=prefix,
        file_type="parquet" 
    )
    example_uri = table_mapping[list(table_mapping.keys())[0]][0]
    root_schema = generate_root_schema(
        bucket=bucket, 
        prefix=prefix,
        example_uri=example_uri
    )
    
    ls_bad_schema = []
    root_iterator = tqdm(table_mapping.items())
    for root, suffix_list in root_iterator:
        root_desc = '/'.join(root.replace(prefix, '').split('/')[1:-1])
        root_iterator.set_description(f'Folder {root_desc}..')
        suffix_iterator = tqdm(suffix_list)
        for suffix in suffix_iterator:
            suffix_iterator.set_description(f'Processing {suffix}..')
            uri = get_gsutil_uri(bucket, suffix)
            df = pd.read_parquet(uri)
            table_schema = generate_pandas_schema(df)
            if table_schema != root_schema:
                table_schema["uri"] = uri
                ls_bad_schema.append(table_schema)
    return ls_bad_schema


def remove_partition_keys(columns: pd.core.indexes.base.Index, uri: str)-> list:
    ls_partition_keys = []
    for part in uri.split('/'):
        if '=' in part:
            ls_partition_keys.append(part.split('=')[0])
    return [col for col in columns if col not in ls_partition_keys], ls_partition_keys


def show_outltiers(row, columns, root_schema):
    print("type(row)")
    print(type(row))
    highlight = 'background-color: red;'
    default = ''
    style_list = []
    for col in columns:
        if getattr(row, col) == root_schema[col]:
            style_list.append(default)
        else:
            style_list.append(highlight)
    return style_list


def keep_divergent_rows(df: pd.DataFrame, all_schema: dict) -> pd.DataFrame():
    query = []
    for col in df_bad.columns:
        if col in all_schema:
            query.append(f"({col}!='{all_schema[col]}')")
    query_str = " | ".join(query)
    query_str
    return df_bad.query(query_str)


def clean_col(value, root_schema, column):
    # if column in value.__dict__.keys():
    if root_schema[column] != value:
        background = "background-color: tomato;"
    else:
        background = ""               
    return background
