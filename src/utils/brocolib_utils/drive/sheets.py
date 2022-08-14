# importing the required libraries
import gspread
import pandas as pd
from credentials import get_creds
from settings import GOOGLE_SHEETS_API_SCOPES

def sheet_to_df(sheet_url, sheet_name):
    
    creds = get_creds(GOOGLE_SHEETS_API_SCOPES)
    
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    
    sheet = client.open_by_url(sheet_url)
    
    for ws in sheet.worksheets():
        if ws.title == sheet_name:
            worksheet = ws
            
    if "worksheet" in locals():
    
        data = worksheet.get_all_records()

        df = pd.DataFrame.from_dict(data)

        return df
    else:
        raise Exception(f"Worksheet '{sheet_name}' not found")
        


def clean_columns_name(dataframe):
    dc_rename = {col:col.replace(' ', '_') for col in dataframe.columns}
    dataframe = dataframe.rename(columns=dc_rename)
    return dataframe
    


def explode_sources(dataframe):
    dataframe["model_source"] = dataframe["model_source"].str.replace(" ", "")
    dataframe["model_source"] = dataframe["model_source"].str.split(',')
    return dataframe.explode("model_source")



def get_sheet_title(sheet_url):
    creds = get_creds(GOOGLE_SHEETS_API_SCOPES)

    # authorize the clientsheet 
    client = gspread.authorize(creds)

    sheet = client.open_by_url(sheet_url)
    
    return sheet.title.replace(' ','_').lower()

