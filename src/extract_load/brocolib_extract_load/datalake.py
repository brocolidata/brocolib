import pandas as pd
from .pubsub import publish_message
from datetime import datetime

def dataframe_to_bucket(dataframe, bucket_name, blob_name, file_type, logger=None):
    '''
    Function load dataframe to bucket
        - Create a blob representation of the dataframe
        - Write dataframe in the blob

    Parameters:
        dataframe (pandas.DataFrame): A dataframe   
        bucket_name (str): Name of the bucket 
        blob_name (str): Name of the blob you want to create
    
    Parameters example:
        blob_name= 'folder/subfolder/filename.csv'
        bucket_name = 'PROJECT_ID-landing'

    Returns:
        gcs_path (str): GCS path where the blob is uploaded
    '''
    gcs_path_temp = f"gs://{bucket_name}/{blob_name}.{{file_extension}}"
    if file_type.lower() == 'csv':
        gcs_path = gcs_path_temp.format(file_extension="csv")
        dataframe.to_csv(gcs_path,index=False)
    elif file_type.lower() == 'parquet':
        gcs_path = gcs_path_temp.format(file_extension="parquet")
        dataframe.to_parquet(gcs_path,index=False)
    elif file_type.lower() == 'json':
        gcs_path = gcs_path_temp.format(file_extension="json")
        dataframe.to_json(gcs_path,index=False)
    else:
        raise NotImplementedError(f"{file_type} is not implemented.")
    if logger:
            logger.info(f'Load Destination : {gcs_path}')
    return gcs_path



def bucket_to_dataframe(bucket_name, blob_name, file_type):
    '''
    Function writes a file into a dataframe     

    Parameters:
      bucket_name (str): Name of the bucket 
      blob_name (str): Name of the blob you want to create 
      file_type (str): Type of the file in the bucket
    
    Returns:
      dataframe (pandas.DataFrame): fetched dataframe
    '''

    file_type = file_type.lower()
    url = f'gs://{bucket_name}/{blob_name}'
    print(f'using {url}')
    if file_type == 'csv':

        return pd.read_csv(url)

class ExternalTable:
    def __init__(
        self, 
        bucket_name,
        partition_keys,
        bucket_file,
        bucket_table_directory,
        bucket_directory,
        dbt_topic,
        gcp_project,
        logger=None
    ):
        self.bucket_name = bucket_name
        self.partition_keys = partition_keys
        self.subfolders = bucket_directory
        self.source_name = bucket_table_directory
        self.bucket_table_directory = bucket_table_directory
        self.file_name = bucket_file
        self.dbt_topic = dbt_topic
        self.gcp_project = gcp_project
        self.logger = logger if logger else None
        self.blob_name = self.format_filename()
        self.gcs_path = None

    def add_partition_keys(self, path_prefix):
        now = datetime.now()
       
        for key, value in self.partition_keys.items():
            if key=="year":
                value = now.year
            elif key=="month":
                value = now.month
            
            path_prefix += f"/{key}={value}"
        return path_prefix


    def format_filename(self):
        now = datetime.now()
        path_prefix=self.add_partition_keys(f"{self.subfolders}/{self.bucket_table_directory}")
        
        return f"{path_prefix}/{self.file_name}_{str(now.day)}"
    
    def to_datalake(self, df, logger=None):
        self.gcs_path = dataframe_to_bucket(
            dataframe=df, 
            bucket_name=self.bucket_name, 
            blob_name=self.blob_name, 
            file_type="parquet",
            logger=logger
        )

    def publish_message(self):
        publish_message(
            sources=[self.source_name],
            dbt_topic=self.dbt_topic,
            gcp_project=self.gcp_project,
            logger=self.logger
        )