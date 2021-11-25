import pandas as pd

def dataframe_to_bucket(dataframe, bucket_name, blob_name, file_type):
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
  gcs_path_temp = f"gs://{bucket_name}/{blob_name}/{{file_extension}}"
  if file_type.lower() == 'csv':
    gcs_path = gcs_path_temp.format(file_extension="csv")
    dataframe.to_csv(gcs_path,index=False)
  elif file_type.lower() == 'parquet':
    gcs_path = gcs_path_temp.format(file_extension="parquet")
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
