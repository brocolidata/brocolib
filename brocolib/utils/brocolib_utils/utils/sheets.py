# importing the required libraries
import os
from functools import lru_cache
import gspread
import gspread_pandas
import pandas as pd
from brocolib_utils import credentials
# from brocolib_utils import settings

def get_sheets_credentials():
    return gspread_pandas.conf.get_creds(
        config=credentials.get_credential_file_asdict()
    )
    # return credentials.get_creds(settings.GOOGLE_SHEETS_API_SCOPES)


# @lru_cache(maxsize=1)
# def get_google_sheet(sheet_id:str) -> gspread.Spreadsheet:
#     creds = get_sheets_credentials()    
#     client = gspread.authorize(creds)
#     google_sheet = client.open_by_key(sheet_id)
#     return google_sheet

# @lru_cache(maxsize=1)
def get_google_sheet(sheet_id:str) -> gspread_pandas.Spread:
    creds = get_sheets_credentials()    
    # client = gspread.authorize(creds)
    google_sheet = gspread_pandas.Spread(spread=sheet_id, creds=creds)
    # google_sheet = client.open_by_key(sheet_id)
    return google_sheet

def get_google_worksheet(
    sheet_id:str, 
    worksheet_name:str
) -> gspread_pandas.Spread:
    creds = get_sheets_credentials()    
    google_worksheet = gspread_pandas.Spread(
        spread=sheet_id, 
        sheet=worksheet_name,
        creds=creds
    )
    return google_worksheet


def clean_columns_name(dataframe):
    dc_rename = {col:col.replace(' ', '_') for col in dataframe.columns}
    dataframe = dataframe.rename(columns=dc_rename)
    return dataframe
    


def explode_sources(dataframe):
    dataframe["model_source"] = dataframe["model_source"].str.replace(" ", "")
    dataframe["model_source"] = dataframe["model_source"].str.split(',')
    return dataframe.explode("model_source")



def get_sheet_title(sheet_url):
    creds = get_sheets_credentials()
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url)
    return sheet.title.replace(' ','_').lower()

