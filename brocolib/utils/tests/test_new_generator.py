import json
import yaml
import os
import pathlib
import pandas as pd
import pytest
from brocolib_utils.fast_dbt import new_generator
from brocolib_utils.ddm import sheet_parser
from brocolib_utils.ddm import ddm_settings

DDM_SHEETS_FOLDER = "ddm_sheet_demo"
DBT_MANIFESTS_FOLDER = "dbt_manifests_demo"
DBT_SQL_FOLDER = "dbt_sql_demo"
DATA_FILES = [
        "SOURCE_TABLES",
        "SOURCE_COLUMNS"
    ]

@pytest.fixture()
def load_demo_data():
    dc_sheets = {}
    sheet = sheet_parser.get_ddm_sheet()
    for str_sheet_name in DATA_FILES:
        parent_dir = pathlib.Path(__file__).parent.resolve()
        base_file_path = os.path.join(parent_dir, DDM_SHEETS_FOLDER, f"{str_sheet_name}_filled.json")
        with open(base_file_path) as f:
            base_data = json.load(f)
        sheet_name = ddm_settings.get_sheet_enum(str_sheet_name)
        df_raw_base = pd.DataFrame(base_data)
        df_base = ddm_settings.format_DDM_dataframe(
                in_df=df_raw_base,
                sheet=sheet_name, 
                format_mode="import"
        )
        sheet_parser.df_to_ddm_sheet(
            df=df_base,
            sheet=sheet,
            sheet_name=sheet_name
        )
        print("debug load demo data", str_sheet_name)
        dc_sheets[str_sheet_name] = df_base
    return dc_sheets

def test_generate_source_yaml_asdict(load_demo_data, populate_bucket):
    bucket = populate_bucket
    dc_sheets = load_demo_data
    sources_dict = new_generator.generate_source_yaml_asdict(
        source_name="test_source",
        datalake_bucket=bucket.name
    )
    parent_dir = pathlib.Path(__file__).parent.resolve()
    test_file_path = os.path.join(parent_dir, DBT_MANIFESTS_FOLDER, "sources.yaml")
    with open(test_file_path) as ff:
        test_dict = yaml.safe_load(ff)
    assert sources_dict["sources"][0]["name"] == test_dict["sources"][0]["name"] 
    assert sources_dict["sources"][0]["tables"][0]["name"] == test_dict["sources"][0]["tables"][0]["name"]
    assert len(sources_dict["sources"][0]["tables"][0]["columns"]) == len(test_dict["sources"][0]["tables"][0]["columns"])



def test_generate_staging_model_sql(load_demo_data, populate_bucket):
    bucket = populate_bucket
    dc_sheets = load_demo_data
    query = new_generator.generate_staging_model_sql(
        source_name="test_source",
        table="test_table"
    )
    parent_dir = pathlib.Path(__file__).parent.resolve()
    test_file_path = os.path.join(parent_dir, DBT_SQL_FOLDER, "staging_model.sql")
    with open(test_file_path, 'r') as f:
        test_query = f.read()
    assert query == test_query


def test_generate_staging_model_yaml():
    dc_model = new_generator.generate_staging_model_yaml(
        source_name="test_source",
        tables=["test_table"]
    )
    parent_dir = pathlib.Path(__file__).parent.resolve()
    test_file_path = os.path.join(parent_dir, DBT_MANIFESTS_FOLDER, "staging_model.yaml")
    with open(test_file_path) as ff:
        test_dict = yaml.safe_load(ff)
    assert dc_model == test_dict


def test_generate_metrics():
    dc_metrics = new_generator.generate_metrics(
        metric_list=["new_customers"]
    )
    parent_dir = pathlib.Path(__file__).parent.resolve()
    test_file_path = os.path.join(parent_dir, DBT_MANIFESTS_FOLDER, "metrics.yaml")
    with open(test_file_path) as ff:
        test_dict = yaml.safe_load(ff)

    assert dc_metrics == test_dict


def test_generate_exposures():
    dc_exposures = new_generator.generate_exposures(
        exposure_list=["MAC03"]
    )
    parent_dir = pathlib.Path(__file__).parent.resolve()
    test_file_path = os.path.join(parent_dir, DBT_MANIFESTS_FOLDER, "exposures.yaml")
    with open(test_file_path) as ff:
        test_dict = yaml.safe_load(ff)

    assert dc_exposures == test_dict
