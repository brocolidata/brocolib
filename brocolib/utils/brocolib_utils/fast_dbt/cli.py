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


import sys
import typer
from collections import OrderedDict
from pprint import pprint
from typing import Optional
# from ruamel import yaml
from ruamel.yaml import YAML
from brocolib_utils.fast_dbt import new_generator

app = typer.Typer()

@app.callback()
def fast_dbt():
    """
    Domain Data Management Sheets Parser & Generator
    """


@app.command()
def generate_source_yaml(
    source_name: Optional[str] = typer.Argument(None, help="dbt source name"),
    datalake_bucket: Optional[str] = typer.Argument(None, help="datalake bucket name where the data is located")
):
    """
    Filling Source Tables & Source Columns worksheets in the DDM Google Sheets
    """

    
    source_name = source_name or typer.prompt("Name of the source ?")
    if not source_name:
        typer.echo('You must provide a source_name. Exiting.')
        raise typer.Exit(code=1)
    

    typer.echo(f"Generating YAML for source : {source_name} ..")
    dc_source = new_generator.generate_source_yaml_asdict(
        source_name=source_name,
        datalake_bucket=datalake_bucket
    )
    new_generator.yaml_to_stdout(dc_source)


@app.command()
def generate_staging_sql(
    source_name: Optional[str] = typer.Argument(None, help="dbt source name"),
    table_name: Optional[str] = typer.Argument(None, help="name of the table")
):
    """
    Generates SQL code for a staging model
    """
    source_name = source_name or typer.prompt("Name of the source ?")
    if not source_name:
        typer.echo('You must provide a source_name. Exiting.')
        raise typer.Exit(code=1)
    
    table_name = table_name or typer.prompt("Name of the table ?")
    if not table_name:
        typer.echo('You must provide a table_name. Exiting.')
        raise typer.Exit(code=1)
    
    query = new_generator.generate_staging_model_sql(
        source_name=source_name,
        table=table_name
    )

    print(query)


@app.command()
def generate_staging_yaml(
    source_name: Optional[str] = typer.Argument(None, help="dbt source name"),
    tables: str = typer.Argument(None, help="name of the table")
):
    """
    Generate YAML for staging models
    """
    source_name = source_name or typer.prompt("Name of the source ?")
    if not source_name:
        typer.echo('You must provide a source_name. Exiting.')
        raise typer.Exit(code=1)
    
    tables = tables or typer.prompt("Coma-separated list of tables (table1,table2) ? ")
    if not tables:
        typer.echo('You must provide tables. Exiting.')
        raise typer.Exit(code=1)
    tables = tables.split(',')
    
    dc_yaml = new_generator.generate_staging_model_yaml(
        source_name=source_name,
        tables=tables
    )
    new_generator.yaml_to_stdout(dc_yaml)