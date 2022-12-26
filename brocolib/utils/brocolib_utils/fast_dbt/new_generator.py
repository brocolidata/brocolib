import sys
from collections import OrderedDict
from ruamel.yaml.scalarstring import DoubleQuotedScalarString 
from ruamel.yaml import YAML
from brocolib_utils.ddm import sheet_parser, sources_parser
from brocolib_utils.ddm import ddm_settings
from brocolib_utils.utils import datalake
from brocolib_utils import settings
import pandas as pd

RAW_SOURCE_SQL = """with source as (
    select * from {{{{ source('{source_name}', '{table_name}') }}}}
),
"""
RAW_PREPARED_SOURCE_SQL = """
prepared_source as (
    select 
        {columns_cast}
    from source
)

select * from prepared_source
"""
COL_CAST_INTERLINES = """,
        """
COL_CAST_FIRST_LINE = ""

def generate_source_yaml_asdict(
    source_name:str,
    datalake_bucket:str = None
):
    dc_source_tables = datalake.get_source(
        source_name=source_name,
        datalake_bucket=datalake_bucket
    )

    all_sources_df, spreadsheet = sheet_parser.ddm_sheet_to_df(
        sheet_name=ddm_settings.DDM_SHEET_NAMES.SOURCES
    )
    source_description = all_sources_df.query(f"source_name=='{source_name}'")["description"].iloc[0] or None
    
    all_tables_df, spreadsheet = sheet_parser.ddm_sheet_to_df(
        sheet_name=ddm_settings.DDM_SHEET_NAMES.SOURCE_TABLES
    )

    all_columns_df, _ = sheet_parser.ddm_sheet_to_df(
        sheet_name=ddm_settings.DDM_SHEET_NAMES.SOURCE_COLUMNS,
        worksheet=spreadsheet
    )
    
    init_dbt_sources_dict = init_dbt_sources(
        database=settings.DATALAKE_PROJECT,
        source_name=source_name,
        source_description=source_description
    )

    dbt_sources_dict = generate_loaded_tables_specs(
        loaded_sources=dc_source_tables,
        init_dbt_sources_dict=init_dbt_sources_dict,
        all_tables=all_tables_df,
        all_columns=all_columns_df
    )

    return dbt_sources_dict

    

def init_dbt_sources(
    database:str, 
    source_name:str,
    source_description:str = None
):
    # dc_dbt_sources = OrderedDict()
    dc_dbt_sources = {}
    # dc_dbt_sources["version"]="2"
    dc_dbt_sources["sources"]=[]
    
    # for source in getattr(sources_dataframe, SOURCE_DATASET_COL).unique():
        # dc_source = OrderedDict()
    dc_source = {}
    dc_source["name"] = source_name
    dc_source["description"] = DoubleQuotedScalarString(source_description)
    dc_source["database"] = database
    dc_source["loader"] = "gcloud storage"
    dc_source["tables"] = []

    dc_dbt_sources["sources"].append(dict(dc_source))
    
    return dc_dbt_sources


def init_dbt_staging():
    dc = OrderedDict()
    # return {"models":[]}
    # return {"version":2, "models":[]}
    dc["version"] = 2
    dc["models"] = []
    return dc


def generate_loaded_tables_specs(
    loaded_sources:dict, 
    init_dbt_sources_dict:dict, 
    all_tables:pd.DataFrame,
    all_columns:pd.DataFrame
):
    for table, path in loaded_sources.items():
        table_description = all_tables.query(f"table_name=='{table}'")["description"].iloc[0]
        dc_table = {}
        dc_table["name"] = table
        dc_table["description"] = DoubleQuotedScalarString(table_description)
        dc_table["external"] = {}
        dc_table["external"]["location"] = DoubleQuotedScalarString(f"{path}*")
        dc_table["external"]["options"] = {}
        dc_table["external"]["options"]["format"] = "parquet"
        dc_table["external"]["options"]["hive_partition_uri_prefix"] = DoubleQuotedScalarString(path)

        # dc_table["external"]["partitions"] = [{"name":"year","data_type":"integer"}, 
        #                                       {"name":"month","data_type":"integer"}]
        

        df_table_columns = all_columns.query(f"table_name=='{table}'")
        dc_table["columns"] = []
        for col in df_table_columns.itertuples():
            dc_table["columns"].append(
                {
                    "name":col.column_name, 
                    "data_type":col.data_type,
                    "description":DoubleQuotedScalarString(col.description)
                }
            )

        
        

        init_dbt_sources_dict["sources"][0]["tables"].append(dc_table)


    return init_dbt_sources_dict


def generate_staging_model_sql(source_name:str, table:str):
    dc_columns = sources_parser.get_all_columns_of_tables(
        tables=[table]
    )
    source_sql = RAW_SOURCE_SQL.format(source_name=source_name, table_name=table)
    
    columns_cast = ""
    for x, col in enumerate(dc_columns[table]):
        endline_coma = COL_CAST_FIRST_LINE if x == 0 else COL_CAST_INTERLINES
        columns_cast += endline_coma + f"cast({col['column_name']} as {col['data_type']}) as {col['column_functional_name']}"
    prepared_source_sql = RAW_PREPARED_SOURCE_SQL.format(columns_cast=columns_cast)
    staging_sql = source_sql + prepared_source_sql
    return staging_sql
        

def generate_staging_model_yaml(source_name:str, tables:list) -> dict:
    dc_columns = sources_parser.get_all_columns_of_tables(
        tables=tables
    )
    all_source_tables_df, spreadsheet = sheet_parser.ddm_sheet_to_df(
        sheet_name=ddm_settings.DDM_SHEET_NAMES.SOURCE_TABLES
    )
    staging_dc = init_dbt_staging()

    for table, columns in dc_columns.items():
        table_description = all_source_tables_df.query(f"table_name=='{table}'")["description"].iloc[0] or None
        dc_table = OrderedDict()
        dc_table["name"] = table
        dc_table["description"] = DoubleQuotedScalarString(table_description)
        dc_table["columns"] = []
        for col in columns:
            dc_col = OrderedDict()
            dc_col["name"] = col["column_functional_name"]
            dc_col["description"] = DoubleQuotedScalarString(col["description"])
            dc_table["columns"].append(dc_col)
        staging_dc["models"].append(dc_table)
    return staging_dc


def yaml_to_stdout(dc:dict):
    yaml = YAML()
    yaml.Representer.add_representer(OrderedDict, yaml.Representer.represent_dict)
    yaml.dump(dc, sys.stdout)