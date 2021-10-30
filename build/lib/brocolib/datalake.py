import pandas as pd

def dataframe_to_bucket(dataframe, bucket_name, blob_name, file_type, project_id=None):
  '''
  Function load dataframe to bucket
    - Create a blob representation of the dataframe
    - Write dataframe in the blob

  Parameters:
    dataframe (pandas.DataFrame): A dataframe   
    bucket_name (str): Name of the bucket 
    blob_name (str): Name of the blob you want to create
    project_id(str, optional): ID of the project 
  
  Parameters example:
    blob_name= 'folder/subfolder/filename.csv'
    bucket_name = 'PROJECT_ID-landing'

  Returns:
    dataframe (pandas.DataFrame): Transformed Dataframe
  '''
  
  file_type = file_type.lower()
  url = f'gs://{bucket_name}/{blob_name}'
  print(f'using {url}')
  if file_type == 'csv':
    
    dataframe.to_csv(f'gs://{bucket_name}/{blob_name}',index=False)



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
