import pandas as pd
import gspread_pandas
from typing import Tuple
from brocolib_utils.settings import DATALAKE_BUCKET
from brocolib_utils.utils import datalake
from . import sheet_parser
from . import ddm_settings

# region Source Tables

def fill_sources_sheets(source_name:str, datalake_bucket: str = None):
    """High level functions that fills all sources sheets

    Args:
        source_name (str): Name of the dbt source
        datalake_bucket (str, optional): GCS bucket where the data is located. Defaults to None.
    """
    all_tables_df, spreadsheet = sheet_parser.ddm_sheet_to_df(
        sheet_name=ddm_settings.DDM_SHEET_NAMES.SOURCE_TABLES
    )
    ls_new_tables, ls_all_tables, _ = get_source_tables(
        all_df=all_tables_df, 
        source_name=source_name, 
        datalake_bucket=datalake_bucket
    )
    fill_source_tables(
        sheet=spreadsheet,
        all_df=all_tables_df, 
        ls_new_tables=ls_new_tables, 
        source_name=source_name
    )
    ls_all_tables.extend(ls_new_tables)
    
    all_columns_df, spreadsheet = sheet_parser.ddm_sheet_to_df(
        sheet_name=ddm_settings.DDM_SHEET_NAMES.SOURCE_COLUMNS,
        worksheet=spreadsheet
    )
    fill_source_columns(
        sheet=spreadsheet,
        all_columns_df=all_columns_df,
        ls_all_tables=ls_all_tables,
        source_name=source_name,
        datalake_bucket=datalake_bucket
    )


def get_source_tables(
    all_df:pd.DataFrame,
    source_name:str,
    datalake_bucket:str = None
) -> Tuple[list, list, dict]:
    """Returns all tables in source, 
    ignoring tables already mentioned in the DDM sheet

    Args:
        all_df (pd.DataFrame): DataFrame of all source tables.
        source_name (str): Name of the dbt source.
        datalake_bucket (str, optional): GCS bucket where the data is located. Defaults to None.

    Returns:
        Tuple[list, list, dict]: list of new tables, list of all tables, dict of sources
    """
    dc_source_tables = datalake.get_source(
        source_name=source_name,
        datalake_bucket=datalake_bucket
    )
    source_df = all_df.query(f"source_name=='{source_name}'")
    ls_all_tables = source_df.table_name.tolist()
    ls_new_tables = [
        t for t in dc_source_tables if t not in ls_all_tables
    ]
    return ls_new_tables, ls_all_tables, dc_source_tables


def fill_source_tables(
    sheet:gspread_pandas.Spread,
    all_df:pd.DataFrame,
    ls_new_tables:list,
    source_name:str
):
    """Fill tables in Sources sheet

    Args:
        sheet (gspread_pandas.Spread): Spreadsheet object.
        all_df (pd.DataFrame): DataFrame of all source tables.
        ls_new_tables (list): List of new tables.
        source_name (str): Name of the dbt source.
    """
    dc = {
        "source_name":[source_name for t in ls_new_tables],
        "table_name":[t for t in ls_new_tables],
        "import_table":[True for t in ls_new_tables],
        "stage_external_table":[False for t in ls_new_tables]
    }
    new_df = pd.DataFrame(dc)
    new_all_df = pd.concat([all_df,new_df], ignore_index=True)
    sheet_parser.df_to_ddm_sheet(
        df=new_all_df,
        sheet=sheet,
        sheet_name=ddm_settings.DDM_SHEET_NAMES.SOURCE_TABLES
    )
    

# endregion


# region Source Columns

def get_source_columns(
    source_name:str,
    table_name:str,
    datalake_bucket:str = None
) -> dict:
    """Get BigQuery schema of a tables

    Args:
        source_name (str): Name of the dbt source.
        table_name (str): Name of the table.
        datalake_bucket (str, optional): GCS bucket where the data is located. Defaults to None.

    Returns:
        dict: Dict of all columns in the table.
    """
    blob = f"{source_name}/{table_name}/"
    gcs_url = datalake.get_gsutil_uri(bucket=datalake_bucket,blob=blob)
    df = pd.read_parquet(gcs_url)
    schema = datalake.generate_bigquery_schema_from_df(df)
    return schema


def get_new_source_columns(
    all_columns_df: pd.DataFrame,
    ls_all_tables: list,
    source_name: str,
    datalake_bucket: str
):
    dc_all_columns = {}
    for table in ls_all_tables:
        if table not in all_columns_df.table_name.tolist():
            dc_all_columns[table] = get_source_columns(
                source_name=source_name,
                table_name=table,
                datalake_bucket=datalake_bucket
            )

    return dc_all_columns


def get_all_columns_of_tables(
    tables:list,
    source_name:str = None
):
    df, worksheet = sheet_parser.ddm_sheet_to_df(
        sheet_name=ddm_settings.DDM_SHEET_NAMES.SOURCE_COLUMNS
    )
    dc_columns = {table:[] for table in tables}
    for table in tables:
        df_table = df.query(f"table_name=='{table}'")
        for col in df_table.itertuples():
            dc_columns[table].append(
                {
                    "column_name":col.column_name,
                    "column_functional_name":col.column_functional_name,
                    "data_type":col.data_type,
                    "description":col.description
                }
            )
    return dc_columns




def fill_source_columns(
    sheet: gspread_pandas.Spread,
    all_columns_df: pd.DataFrame,
    ls_all_tables:list,
    source_name:str, 
    datalake_bucket:str = None
):
    
    datalake_bucket = datalake_bucket or DATALAKE_BUCKET
    dc_all_columns = get_new_source_columns(
        all_columns_df=all_columns_df,
        ls_all_tables=ls_all_tables,
        datalake_bucket=datalake_bucket,
        source_name=source_name,
    )
    dc = {
        "table_name":[],
        "column_name":[],
        "data_type":[]

    }
    for table, col_list in dc_all_columns.items():
        for col in col_list:
            dc["table_name"].append(table)
            dc["column_name"].append(col["name"])
            dc["data_type"].append(col["type"])

    new_df = pd.DataFrame(dc)
    new_all_df = pd.concat([all_columns_df,new_df], ignore_index=True)
    sheet_parser.df_to_ddm_sheet(
        df=new_all_df,
        sheet=sheet,
        sheet_name=ddm_settings.DDM_SHEET_NAMES.SOURCE_COLUMNS
    )



# endregion
