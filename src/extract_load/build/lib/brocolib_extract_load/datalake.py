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
        if logger:
            logger.info(f'Load Destination : {gcs_path}')
        dataframe.to_csv(gcs_path,index=False)
    elif file_type.lower() == 'parquet':
        gcs_path = gcs_path_temp.format(file_extension="parquet")
        if logger:
            logger.info(f'Load Destination : {gcs_path}')
        dataframe.to_parquet(gcs_path,index=False)
    else:
        return NotImplementedError(f"{file_type} is not implemented.")
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
        partitionning_keys,
        bucket_file,
        bucket_directory ,
        logger=None
    ):
    
        self.bucket_name = bucket_name
        self.partitionning_keys = partitionning_keys
        self.subfolders = bucket_directory
        self.source_name = bucket_file
        self.file_name = bucket_file
        self.logger = logger if logger else None
        self.blob_name = self.format_filename()
        self.gcs_path = None


    def format_filename(self):
        now = datetime.now()
        year =  now.year
        month =  now.month
        day = now.day

        return f"{self.subfolders}/{self.file_name}/year={year}/month={month}/{self.file_name}_{str(day)}"
    
    def to_datalake(self, df, logger=None):

        self.gcs_path = dataframe_to_bucket(
            dataframe=df, 
            bucket_name=self.bucket_name, 
            blob_name=self.blob_name, 
            file_type="parquet",
            logger=logger
        )

    def publish_message(self):
        publish_message([self.source_name], self.logger)