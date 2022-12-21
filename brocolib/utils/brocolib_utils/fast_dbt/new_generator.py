from ruamel.yaml.scalarstring import DoubleQuotedScalarString 
from brocolib_utils.fast_dbt.ddm import sources_parser, sheet_parser
from brocolib_utils.fast_dbt.ddm import settings as codegen_settings
from brocolib_utils.datalake import datalake
from brocolib_utils import settings
import pandas as pd

def generate_source_yaml_asdict(
    source_name:str,
    datalake_bucket:str = None
):
    dc_source_tables = datalake.get_source(
        source_name=source_name,
        datalake_bucket=datalake_bucket
    )

    all_sources_df, spreadsheet = sheet_parser.ddm_sheet_to_df(
        sheet_name=codegen_settings.DDM_SHEET_NAMES.SOURCES
    )
    source_description = all_sources_df.query(f"source_name=='{source_name}'")["description"].iloc[0] or None
    
    all_tables_df, spreadsheet = sheet_parser.ddm_sheet_to_df(
        sheet_name=codegen_settings.DDM_SHEET_NAMES.SOURCE_TABLES
    )

    all_columns_df, _ = sheet_parser.ddm_sheet_to_df(
        sheet_name=codegen_settings.DDM_SHEET_NAMES.SOURCE_COLUMNS,
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
    dc_dbt_sources["version"]="2"
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