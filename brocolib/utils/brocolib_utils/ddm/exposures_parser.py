from typing import Tuple
from gspread_pandas import Spread
from . import ddm_settings, sheet_parser
import pandas as pd


def get_all_exposures() -> Tuple[pd.DataFrame, Spread]:
    all_exposures_df, spreadsheet = sheet_parser.ddm_sheet_to_df(
        sheet_name=ddm_settings.DDM_SHEET_NAMES.DASHBOARDS
    )

    return all_exposures_df, spreadsheet


def get_exposures(exposure_list:list):
    all_exposures_df, _ = get_all_exposures()
    exposures_df = all_exposures_df.query("exposure_name.isin(@exposure_list)")

    return exposures_df