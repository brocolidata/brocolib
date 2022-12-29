import pandas as pd
from enum import Enum
from typing import Literal
import os
## Conventions & Defaults for Domain Data Management


DDM_SHEETS_ID = os.getenv('DDM_SHEETS_ID')
DDM_SHEETS_URL = f"https://docs.google.com/spreadsheets/d/{DDM_SHEETS_ID}"

class DDM_SHEET_NAMES(Enum):
    """Domain Data Management default
    names for Google Sheets sheet names
    """
    SOURCES = "Sources"
    DOMAINS = "Domaines"
    SOURCE_TABLES = "Tables sources"
    SOURCE_COLUMNS = "Colonnes sources"
    ENTITIES = "Entites"
    METRICS = "Metriques"
    DASHBOARDS = "Dashboards"


def get_sheet_enum(member:str) -> DDM_SHEET_NAMES:
    return DDM_SHEET_NAMES.__members__.get(member)

def get_sheet_name(member:DDM_SHEET_NAMES) -> str:
    return member.value




## Mapping for Domain Data Management

SOURCE_TABLES_MAPPING = {
    "nom source":"source_name",
    "nom table":"table_name",
    "nom fonctionnel table":"table_functional_name",
    "description":"description",
    "tags":"tags",
    "periode actualisation":"actualisation_period",
    "importer":"import_table",
    "stage_external_table":"stage_external_table",
    "frequence":"frequence",
    "specs":"specs"
}

SOURCE_COLUMNS_MAPPING = {
    "nom table":"table_name",
    "nom colonne":"column_name",
    "nom fonctionnel colonne":"column_functional_name",
    "type donnee":"data_type",
    "description":"description",
    "tags":"tags"
}

SOURCES_MAPPING = {
    "nom source":"source_name",
    "description":"description"
}

METRICS_MAPPING = {
    "nom metric":"metric_name",
    "label":"label",
    "description":"description",
    "formule":"formula",
    "info":"info",
    "model":"model",
    "method_calcul":"calculation_method",
    "expression":"expression",
    "timestamp":"timestamp",
    "time_grains":"time_grains",
    "dimensions":"dimensions",
    "filters":"filters",
    "window":"window",
    "treat_null_values_as_zero":"treat_null_values_as_zero",
    "enabled":"enabled"
}

DASHBOARDS_MAPPING = {
    "nom exposure":"exposure_name",
    "label exposure":"exposure_label",
    "type exposure":"exposure_type",
    "maturite":"maturity",
    "url":"url",
    "description":"description",
    "depend de":"depends_on",
    "nom responsable ":"owner_name",
    "email responsable ":"owner_email",
    "acces":"access"
}

def format_DDM_dataframe(
    in_df:pd.DataFrame,
    sheet: DDM_SHEET_NAMES, 
    format_mode: Literal['import', 'export']
) -> pd.DataFrame:
    """Rename columns in pandas DataFrame from/to 
    Google Sheets DDM format.

    Args:
        in_df (pd.DataFrame): DataFrame to format
        sheet (DDM_SHEET_NAMES): a member of DDM_SHEET_NAMES enum
        format_mode (str): One of "import" or "export".

    Raises:
        ValueError: if format_mode is incorrect

    Returns:
        pd.DataFrame: DataFrame formated
    """
    mapping_name = f"{sheet.name}_MAPPING"
    sheet_mapping_dict = globals().get(mapping_name)
    if format_mode == "import":
        mapping_dict = sheet_mapping_dict
    elif format_mode == "export":
        mapping_dict ={v:k for k,v in sheet_mapping_dict.items()}
    else:
        raise ValueError('format_mode must be one of ["import","export"]')
    out_df = in_df.rename(columns=mapping_dict)

    return out_df