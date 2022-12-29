from typing import Tuple
from gspread_pandas import Spread
from . import ddm_settings, sheet_parser
import pandas as pd


def get_all_metrics() -> Tuple[pd.DataFrame, Spread]:
    all_metrics_df, spreadsheet = sheet_parser.ddm_sheet_to_df(
        sheet_name=ddm_settings.DDM_SHEET_NAMES.METRICS
    )

    return all_metrics_df, spreadsheet


def get_metrics(metric_list:list):
    all_metrics_df, _ = get_all_metrics()
    metrics_df = all_metrics_df.query("metric_name.isin(@metric_list)")

    return metrics_df