import pandas as pd

def extract(url, source_type):
  '''
  Function to extract data
    - read json from url
    - convert json to dataframe

  Parameters:
    url (str): url of the data source      
    source_type (str): type of the data to fetch

  Returns:
     (pandas.DataFrame): Dataframe created from source

  Exceptions:
      NotImplementedError: if the source type is not implemented 
  '''
  source_type = source_type.lower()

  if source_type == 'json':
    return pd.read_json(url)
  
  else:
    raise NotImplementedError("sources available: json")