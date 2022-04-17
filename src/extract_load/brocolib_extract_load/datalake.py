import pandas as pd
from .pubsub import publish_sources
from datetime import datetime


def dataframe_to_bucket(
    dataframe: pd.DataFrame, 
    bucket_name: str, 
    blob_name: str, 
    file_type: str, 
    logger=None
) -> str:
    """Loads a DataFrame to a GCS bucket

    Args:
        dataframe (pd.DataFrame): DataFrame you want to upload to GCS
        bucket_name (str): Name of the destination bucket
        blob_name (str): Name of the destination file
        file_type (str): File format
        logger (optional): Logging interface. Defaults to None.

    Parameters example:
        blob_name= 'folder/subfolder/filename.csv'
        bucket_name = 'PROJECT_ID-landing'


    Raises:
        NotImplementedError: If the file format is not implemented

    Returns:
        str: GCS path where the blob is uploaded
    """
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



def bucket_to_dataframe(bucket_name: str, blob_name: str, file_type: str) -> pd.DataFrame:
    '''
    Loads a file located in a GCS bucket into a DataFrame     

    Parameters:
      bucket_name (str): Name of the source bucket 
      blob_name (str): Name of the blob in the source bucket
      file_type (str): Type of the file in the bucket
    
    Returns:
      pandas.DataFrame: fetched DataFrame
    '''

    file_type = file_type.lower()
    url = f'gs://{bucket_name}/{blob_name}'
    print(f'using {url}')
    if file_type == 'csv':

        return pd.read_csv(url)

class ExternalTable:
    def __init__(
        self, 
        bucket_name: str,
        partition_keys: dict,
        bucket_file: str,
        bucket_table_directory: str,
        bucket_directory: str,
        dbt_topic: str,
        gcp_project: str,
        logger=None
    ):
        """Instanciate a ExternalTable object

        Args:
            bucket_name (str): Name of the the GCS bucket where the data is located
            partition_keys (dict): Pairs of partition keys and values
            bucket_file (str): Name of the file in GCS bucket
            bucket_table_directory (str): Name of the directory after which the ExternalTable is named
            bucket_directory (str): Name of the subdirectories under the bucket's root level
            dbt_topic (str): Name of the Pub/Sub dbt topic
            gcp_project (str): Namae of the GCP project
            logger (_type_, optional): Logging interface. Defaults to None.
        """
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

    def add_partition_keys(self, path_prefix: str) -> str:
        """Add partition_keys in Hive Format to a GCS path prefix

        Args:
            path_prefix (str) : GCS path prefix

        Returns:
            str: GCS Path prefix appended by partition keys
        """
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
        publish_sources(
            sources=[self.source_name],
            dbt_topic=self.dbt_topic,
            gcp_project=self.gcp_project,
            logger=self.logger
        )