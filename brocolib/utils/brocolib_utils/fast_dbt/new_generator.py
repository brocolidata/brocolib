import sys
import re
from io import StringIO
from typing import Union
from collections import OrderedDict
from ruamel.yaml.scalarstring import DoubleQuotedScalarString 
from ruamel.yaml import YAML
from brocolib_utils.ddm import sheet_parser, sources_parser, metrics_parser, exposures_parser
from brocolib_utils.ddm import ddm_settings
from brocolib_utils.utils import datalake
from brocolib_utils import settings
import pandas as pd

# region Generic

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
REGEX_METRICS_FIlTER = r"(?P<field>[\D\_]*)\s(?P<operator>is|\=|\>|\<|\>\=|\<\=|\!\=|\<\>)\s(?P<value>\'?.*\'?)"
REGEX_METRICS_WINDOW = r"(?P<count>[\d]*)\s(?P<period>day|week|month|year|all_time)s?"

def yaml_to_stdout(dc:dict):
    yaml = YAML()
    yaml.Representer.add_representer(OrderedDict, yaml.Representer.represent_dict)
    yaml.dump(dc, sys.stdout)

def object_to_yaml_str(obj:Union[dict, OrderedDict], options=None) -> str:
    yaml = YAML()
    yaml.Representer.add_representer(OrderedDict, yaml.Representer.represent_dict)
    if options == None: options = {}
    string_stream = StringIO()
    yaml.dump(obj, string_stream, **options)
    output_str = string_stream.getvalue()
    string_stream.close()
    return output_str

# endregion

# region Sources
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
    version: int = 2,
    source_description:str = None
):
    # dc_dbt_sources = OrderedDict()
    dc_dbt_sources = {}
    dc_dbt_sources["version"]=version
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
# endregion

# region Staging

def init_dbt_staging(version: int = 2):
    dc = OrderedDict()
    # return {"models":[]}
    # return {"version":2, "models":[]}
    dc["version"] = version
    dc["models"] = []
    return dc


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
# endregion

# region Metrics


def init_dbt_metrics(version: int = 2):
    return OrderedDict(
        version = version,
        metrics = []
    )


def process_filters(metric_filters):
    ls_filters = []
    for filt in metric_filters.split(',\n'):
        re_matchs = re.match(REGEX_METRICS_FIlTER, filt.strip(), flags=re.IGNORECASE)
        matchs = re_matchs.groupdict()
        ls_filters.append(
            OrderedDict(
                field = matchs["field"],
                operator = matchs["operator"],
                value = matchs["value"]
            )  
        )
    return ls_filters


def process_window(raw_window):
    re_matchs = re.match(REGEX_METRICS_WINDOW, raw_window, flags=re.IGNORECASE)
    matchs = re_matchs.groupdict()
    return OrderedDict(
        count = matchs["count"],
        period = matchs["period"]
    )


def generate_metrics(metric_list:list):
    df_metrics = metrics_parser.get_metrics(metric_list)
    metrics_dc = init_dbt_metrics()

    for metric in df_metrics.itertuples():
        metric_orderdict = OrderedDict(
            name = metric.metric_name,
            label = metric.label,
            model = metric.model,
            description = DoubleQuotedScalarString(metric.description),
            calculation_method = metric.calculation_method,
            expression = metric.expression,
            timestamp = metric.timestamp,
            time_grains = [tg.strip() for tg in metric.time_grains.split(',')],
            dimensions = [d.strip() for d in metric.dimensions.split(',')],
            filters = process_filters(metric.filters),
            window = process_window(metric.window)
        )
        metric_orderdict["config"] = OrderedDict(
            treat_null_values_as_zero = metric.treat_null_values_as_zero,
            enabled  = metric.enabled
        )
        metrics_dc["metrics"].append(metric_orderdict)
    return metrics_dc

# endregion

# region Exposures

def init_dbt_exposures(version: int = 2):
    return OrderedDict(
        version = version,
        exposures = []
    )


def generate_exposures(exposure_list:list):
    df_exposures = exposures_parser.get_exposures(exposure_list)
    exposures_dc = init_dbt_exposures()

    for exposure in df_exposures.itertuples():
        exposure_orderdict = OrderedDict(
            name = exposure.exposure_name,
            label = DoubleQuotedScalarString(exposure.exposure_label),
            maturity = exposure.maturity,
            url = exposure.url,
            description = DoubleQuotedScalarString(exposure.description),
            depends_on = [do.strip() for do in exposure.depends_on.split(',')]
        )
        exposure_orderdict["owner"] = OrderedDict(
            name = exposure.owner_name,
            email  = exposure.owner_email
        )
        exposures_dc["exposures"].append(exposure_orderdict)
    return exposures_dc

# endregion