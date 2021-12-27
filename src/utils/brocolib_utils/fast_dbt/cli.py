import os
import argparse
from brocolib_utils.settings import (ALL_FIELDS_SHEET_NAME, SOURCES_SHEET_NAME, 
                                get_project_settings, DBT_MODELS_PATH)
from brocolib_utils.drive.sheets import sheet_to_df, clean_columns_name
from brocolib_utils.fast_dbt.generator import (get_loaded_sources, init_dbt_sources, 
                                generate_loaded_tables_specs, 
                                dict_to_yaml)
from brocolib_utils.datalake import get_sources

from collections import OrderedDict

from utils.brocolib_utils import datalake

# Create the parser
my_parser = argparse.ArgumentParser(description='Generate diagrams for a DWH spec')

datalake_bucket = os.environ.get('DATALAKE_BUCKET')
gcp_project = os.environ.get('PROJECT_ID')
first_partition_key = os.environ.get('DEFAULT_GCS_PARTITIONNING_KEYS')[0]
sources_dict = get_sources(
    gcp_project=gcp_project,
    datalake_bucket=datalake_bucket,
    first_partition_key=first_partition_key
)

init_dbt_sources_dict = init_dbt_sources(
    database=gcp_project, 
    loader=None, 
    version=2
)


dbt_sources_dict = generate_loaded_tables_specs(
    loaded_sources=sources_dict,
    init_dbt_sources_dict=init_dbt_sources_dict
)


dict_to_yaml(yaml_dict=dbt_sources_dict, yaml_file_path=f"{DBT_MODELS_PATH}/stg.yml")

print('successfully generated stg.yml !')