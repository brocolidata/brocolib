import json
import pathlib
import os
import pandas as pd
import pytest
from brocolib_utils.ddm import sources_parser, sheet_parser
from brocolib_utils.ddm import ddm_settings
# from .conftest import populate_bucket

def test_no_import_error():
    from brocolib_utils.fast_dbt import generator
    pass

DATA_FILES_FOLDER = "ddm_sheet_demo"
DATA_FILES = [
        "SOURCE_TABLES",
        "SOURCE_COLUMNS"
    ]

@pytest.fixture()
def get_expectated_data():
    dc_expectations = {}
    for str_sheet_name in DATA_FILES:
        parent_dir = pathlib.Path(__file__).parent.resolve()
        file_path = os.path.join(parent_dir, DATA_FILES_FOLDER, f"{str_sheet_name}.json")
        with open(file_path) as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        dc_expectations[str_sheet_name] = df
    return dc_expectations


@pytest.fixture()
def load_demo_data():
    dc_sheets = {}
    sheet = sheet_parser.get_ddm_sheet()
    for str_sheet_name in DATA_FILES:
        parent_dir = pathlib.Path(__file__).parent.resolve()
        base_file_path = os.path.join(parent_dir, DATA_FILES_FOLDER, f"{str_sheet_name}_base.json")
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


def test_format_DDM_dataframe(load_demo_data):
    dc_sheets = load_demo_data
    for str_sheet_name, df in dc_sheets.items():
        sheet = ddm_settings.get_sheet_enum(str_sheet_name)
        import_format_df = ddm_settings.format_DDM_dataframe(
            in_df=df,
            sheet = sheet,
            format_mode="import"
        )

        mapping = getattr(ddm_settings, f"{sheet.name}_MAPPING")
        assert import_format_df.columns.tolist() == list(mapping.values())

        export_format_df = ddm_settings.format_DDM_dataframe(
            in_df=import_format_df,
            sheet = sheet,
            format_mode="export"
        )
        assert export_format_df.columns.tolist() == list(mapping.keys())


def test_fill_source_tables(populate_bucket, load_demo_data, get_expectated_data):
    bucket = populate_bucket
    dc_sheet = load_demo_data
    dc_expectations = get_expectated_data
    sources_parser.fill_sources_sheets(
        source_name="test_source", 
        datalake_bucket=bucket.name
    )
    for str_sheet_name in dc_sheet:
        sheet_name = ddm_settings.get_sheet_enum(str_sheet_name)
        df_test, _ = sheet_parser.ddm_sheet_to_df(
            sheet_name=sheet_name
        )

        df_test_formated = ddm_settings.format_DDM_dataframe(
            in_df=df_test,
            sheet=sheet_name,
            format_mode="export"
        )
        df = dc_expectations[str_sheet_name]
        filled_tables = df_test_formated.to_dict(orient="records")
        assert filled_tables == df.to_dict(orient="records")