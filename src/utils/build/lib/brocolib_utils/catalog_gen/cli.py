from email.policy import default
import os
import argparse
from brocolib_utils.catalog_gen.dbt_catalog import (generate_dbt_docs, get_dbt_populated_index, run_dbt_debug,
    run_dbt_deps)



my_parser = argparse.ArgumentParser(description='List the content of a folder')


my_parser.add_argument(
    '--profile-path',
    metavar='profile_path',
    type=str,
    help='dbt project path',
    default=os.environ.get('DBT_PROFILES_DIR')
)

my_parser.add_argument(
    '--project-path',
    metavar='project_path',
    type=str,
    help='dbt profile path',
    default=os.environ.get('DBT_PATH')
)

my_parser.add_argument(
    '--target-path',
    metavar='target_path',
    type=str,
    help='dbt target path',
    default='/tmp/target'
)

my_parser.add_argument(
    '--debug',
    metavar='debug',
    type=bool,
    help='enable debug',
    default=False
)

my_parser.add_argument(
    '--ci',
    metavar='is_ci',
    type=bool,
    help='if the runtime is a CI/CD pipeline',
    default=False
)

args = my_parser.parse_args()

project_path = args.project_path
profile_path = args.profile_path
target_path = args.target_path
is_CI = args.ci
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