# import os
# import json
# import argparse
# from ruamel.yaml import YAML

# from dbt_parser import update_exposures 
# from ruamel.yaml import YAML

# from dbt_parser import update_exposures 
# from brocolib_utils.settings import DBT_MODELS_PATH
# from brocolib_utils.fast_dbt.generator import (init_dbt_sources, 
#     generate_loaded_tables_specs, dict_to_yaml)
# from brocolib_utils.datalake import get_sources
# from collections import OrderedDict

# DATALAKE_BUCKET = os.environ.get('DATALAKE_BUCKET')
# GCP_PROJECT = os.environ.get('BACK_PROJECT_ID')
# DEFAULT_GCS_PARTITIONNING_KEYS = json.loads(os.environ.get('DEFAULT_GCS_PARTITIONNING_KEYS'))



# def main():

#     # Create the parser
#     fast_dbt_parser = argparse.ArgumentParser(description='fast_dbt Python CLI ')
#     command_parser = fast_dbt_parser.add_subparsers(dest='command')
    
#     ## Exposures
#     exposure_parser = command_parser.add_parser('exposure', help='Manage exposures')
#     exposure_subcommand_parser = exposure_parser.add_subparsers(dest='exposure_subcommand')
#     update_permissions_parser = exposure_subcommand_parser.add_parser('update_permissions', help='Parse dbt exposure .yml file and update data studio permissions')
#     update_permissions_parser.add_argument(
#         'file-path',
#         dest='exposure_file_path',
#         help='path to the dbt exposures .yml file'
#     )

#     args = fast_dbt_parser.parse_args()

#     if args.command == "exposure":
#         if args.exposure_subcommand = "update_permissions"
#             yaml_parser = YAML()
#             with open(args.exposure_file_path, 'r') as f:
#                 data = yaml_parser.load(f)
#             update_exposures(data)


