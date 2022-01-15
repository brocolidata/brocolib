from email.policy import default
import os
import argparse
from brocolib_utils.catalog_gen.dbt_catalog import (generate_dbt_docs, get_dbt_populated_index, run_dbt_debug,
    run_dbt_deps, upload_populated_index)



my_parser = argparse.ArgumentParser(description='List the content of a folder')


my_parser.add_argument(
    '--target-path',
    dest='target_path',
    type=str,
    help='dbt target path',
    default='/tmp/target'
)

my_parser.add_argument(
    '--debug',
    dest='debug'
    type=bool,
    help='enable debug',
    action="store_true"
)

my_parser.add_argument(
    '--ci',
    dest='is_CI'
    type=bool,
    help='if the runtime is a CI/CD pipeline',
    action="store_true"
)

args = my_parser.parse_args()

target_path = args.target_path
is_CI = args.is_CI
debug = args.debug

if is_CI:
    run_dbt_deps()

if debug:
    run_dbt_debug()

generate_dbt_docs()


new_content = get_dbt_populated_index(
    target_folder=target_path
)

upload_populated_index(
    content=new_content
)