import os
import gspread
from credentials import get_creds

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

GOOGLE_SHEETS_API_SCOPES = [
    'https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'
]

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

    
