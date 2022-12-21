from google.cloud import storage

def get_storage_client(gcp_project):
    return storage.Client(project=gcp_project)

def add_to_source_list(
    client, 
    datalake_bucket, 
    first_partition_key,
    prefix="", 
    ls_sources=[]
):
    result = client.list_blobs(
        bucket_or_name=datalake_bucket,
        prefix=prefix,
        delimiter='/'
    )
    for element in result:
        pass
    
    for element in result.prefixes:
        if f"{first_partition_key}=" in element:
            ls_sources.append(prefix)
        else:
            add_to_source_list(
                client=client,
                datalake_bucket=datalake_bucket,
                first_partition_key=first_partition_key,
                prefix=element, 
                ls_sources=ls_sources
            )
    return ls_sources


def add_to_source_list(
    client, 
    datalake_bucket, 
    first_partition_key,
    prefix="", 
    sources_dict={}
):
    result = client.list_blobs(
        bucket_or_name=datalake_bucket,
        prefix=prefix,
        delimiter='/'
    )
    for element in result:
        pass
    
    for element in result.prefixes:
        if element.replace(prefix, "").startswith(f"{first_partition_key}="):
            table_name = prefix.split('/')[-2]
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
    


def get_raw_sources(gcp_project, datalake_bucket, first_partition_key):
    client = get_storage_client(gcp_project)
    sources_dict=add_to_source_list(
        client=client,
        datalake_bucket=datalake_bucket,
        first_partition_key=first_partition_key
    )
    return sources_dict


def get_sources(gcp_project, datalake_bucket, first_partition_key):
    raw_sources_dict = get_raw_sources(gcp_project, datalake_bucket, first_partition_key)
    sources_dict = {table:f"gs://{datalake_bucket}/{blob}" for table, blob in raw_sources_dict.items()}
    return sources_dict



    
