import os
import json
import argparse
from brocolib_utils.settings import DBT_MODELS_PATH
from brocolib_utils.fast_dbt.generator import (init_dbt_sources, 
    generate_loaded_tables_specs, dict_to_yaml)
from brocolib_utils.datalake import get_sources

from collections import OrderedDict

# Create the parser
my_parser = argparse.ArgumentParser(description='Generate diagrams for a DWH spec')

DATALAKE_BUCKET = os.environ.get('DATALAKE_BUCKET')
GCP_PROJECT = os.environ.get('BACK_PROJECT_ID')
DEFAULT_GCS_PARTITIONNING_KEYS = json.loads(os.environ.get('DEFAULT_GCS_PARTITIONNING_KEYS'))
first_partition_key = DEFAULT_GCS_PARTITIONNING_KEYS[0]
sources_dict = get_sources(
    gcp_project=GCP_PROJECT,
    datalake_bucket=DATALAKE_BUCKET,
    first_partition_key=first_partition_key
)

init_dbt_sources_dict = init_dbt_sources(
    database=GCP_PROJECT, 
    loader=None, 
    version=2
)


dbt_sources_dict = generate_loaded_tables_specs(
    loaded_sources=sources_dict,
    init_dbt_sources_dict=init_dbt_sources_dict
)


dict_to_yaml(yaml_dict=dbt_sources_dict, yaml_file_path=f"{DBT_MODELS_PATH}/stg.yml")

print('successfully generated stg.yml !')