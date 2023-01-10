import os
from typing import Literal

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
# DBT_MODELS_PATH = f"{os.environ.get('DBT_PATH')}/models"
DATALAKE_PROJECT = os.environ.get('BACK_PROJECT_ID')
DATALAKE_BUCKET = os.environ.get('DATALAKE_BUCKET')
GOOGLE_SHEETS_API_SCOPES = [
    'https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'
]

DATA_STUDIO_API_BASE_URL = "https://datastudio.googleapis.com/v1"
DATA_STUDIO_API_SCOPE = [
    'https://www.googleapis.com/auth/datastudio',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/admin.directory.user',
    'https://www.googleapis.com/auth/admin.directory.group',
    'openid'
]

DATA_STUDIO_ASSETS_TYPES = Literal['REPORT', 'DATA_SOURCE']

BIGQUERY_MAPPING_TYPES = {
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

    
DATA_CATALOG_RELEASE_INDEX_URL = "https://github.com/brocolidata/dbt-docs/releases/latest/download/index.html"