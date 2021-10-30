import pandas as pd

def transform(dataframe, numeric_col, date_col, date_format_str, keep_col=None):
  '''
  Function to transform dataframe
    - transpose dataframe
    - reset and drop the index of dataframe 
    - set numeric columns to numeric
    - set date column to date

  Parameters:
    dataframe (pandas.DataFrame): A dataframe   
    numeric_col(list): A list of column names containing numbers
    date_col (list): A list of column names containing dates     
    date_format_str (str): A datetime formatting string
    keep_col (list): A list of column names to keep 
    

  Returns:
    dataframe (pandas.DataFrame): Transformed Dataframe
    
  '''
  test_list = keep_col + numeric_col + date_col
  test_list_2 = numeric_col + date_col
  
  for col in test_list_2:
    if col not in keep_col:
      raise ValueError(f'{col} not in cols provided in keep_col')

  dataframe = dataframe.transpose()

  for col in test_list:
    if col not in dataframe.columns:
      raise ValueError(f'{col} not in dataframe')
  
  if keep_col:
    
    dataframe = dataframe[keep_col]
  
  
  dataframe[numeric_col] = dataframe[numeric_col].apply(pd.to_numeric)
  # dataframe[date_col] = pd.to_datetime(dataframe[date_col], format=date_format_str)
  dataframe[date_col] = dataframe[date_col].apply(pd.to_datetime, format=date_format_str)
  dataframe = dataframe.reset_index(drop=True)
  
  return dataframe


  

  