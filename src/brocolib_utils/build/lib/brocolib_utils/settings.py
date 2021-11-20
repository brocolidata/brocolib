import os
import gspread
from brocolib_utils.drive import get_creds, GOOGLE_APPLICATION_CREDENTIALS, SCOPE

SCOPE = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
ALL_FIELDS_SHEET_NAME = "all_fields"
GROUP_TABLE_COL = "table_group"
DESCRIPTION_COL = "description"
TABLE_NAME_COL = "table_name"
SOURCE_DATASET_COL = "source_dataset"
FIELD_NAME_COL = "field_name"
FIELD_DESCRIPTION_COL = "field_description"
FILE_FORMAT_COL = "file_format"
GCS_PREFIX_COL = "cloud_storage_prefix"
SOURCES_SHEET_NAME = "sources"
DBT_MODELS_SHEET_NAME = "dbt_models"
DBT_MODELS_PATH = f"{os.environ.get('DBT_PATH')}/models"

def get_project_settings(sheet_url, settings_worksheet_name="project_settings"):
    creds = get_creds()
    
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url)
    for ws in sheet.worksheets():
        if ws.title == settings_worksheet_name:
            settings_worksheet = ws
    settings_dict = {}
    for dico in settings_worksheet.get_all_records():
        settings_dict[dico["setting"]] = dico["value"]

    return settings_dict

MAPPING_TYPES = {
    "integer":"integer",
    "timestamp without time zone":"timestamp",
    "boolean":"bool",
    "character varying":"string",
    "text":"string",
    "date":"date",
    "double precision": "float64",
    "numeric":"numeric",
    "bytea":"bytes",
    "bigint": "bigint"
}

    
