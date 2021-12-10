import pandas as pd
import requests as rq

def extract(url, source_type, nested_key=None):
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
    if nested_key:
      response = rq.get(url)
      data = response.json()[nested_key]
      return pd.DataFrame(data)
    else:
      return pd.read_json(url)
  
  else:
    raise NotImplementedError("sources available: json")