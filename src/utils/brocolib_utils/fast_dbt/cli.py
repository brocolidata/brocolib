import argparse
import yaml
from os import set_blocking
from brocolib_utils.settings import (ALL_FIELDS_SHEET_NAME, SOURCES_SHEET_NAME, 
                                get_project_settings, DBT_MODELS_PATH)
from brocolib_utils.drive import sheet_to_df, clean_columns_name
from brocolib_utils.fast_dbt.generator import (get_loaded_sources, init_dbt_sources, 
                                generate_loaded_tables_specs, 
                                dict_to_yaml)

from collections import OrderedDict

# Create the parser
my_parser = argparse.ArgumentParser(description='Generate diagrams for a DWH spec')

# Add the arguments
my_parser.add_argument(
    'sheet_url',
    metavar='sheet_url',
    type=str,
    help='Google Sheets URl'
)



# Execute the parse_args() method
args = my_parser.parse_args()
sheet_url = args.sheet_url


df_fields = sheet_to_df(sheet_url, ALL_FIELDS_SHEET_NAME)
df_fields = clean_columns_name(df_fields)
df_dbt = sheet_to_df(sheet_url, SOURCES_SHEET_NAME)
df_dbt = clean_columns_name(df_dbt)
loaded_sources = get_loaded_sources(df_dbt)
project_settings_dict = get_project_settings(sheet_url)
init_dbt_sources_dict = init_dbt_sources(
    sources_dataframe=df_dbt,
    database=project_settings_dict["back_project"], 
    loader=None, 
    version=2
)
dbt_sources_dict = generate_loaded_tables_specs(
    loaded_sources=loaded_sources,
    fields_dataframe=df_fields, 
    source_dataframe=df_dbt, 
    init_dbt_sources_dict=init_dbt_sources_dict
)

# yaml.add_representer(OrderedDict, represent_ordereddict)
# yaml.add_representer(str, quoted_presenter)


dict_to_yaml(yaml_dict=dbt_sources_dict, yaml_file_path=f"{DBT_MODELS_PATH}/stg.yml")

print('successfully generated stg.yml !')