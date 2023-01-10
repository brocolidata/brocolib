from gspread import Spreadsheet
from typing import Tuple
from gspread_pandas import Spread
import pandas as pd
from brocolib_utils.utils import sheets
from . import ddm_settings

def get_ddm_sheet() -> Spread:
    return sheets.get_google_sheet(
        sheet_id=ddm_settings.DDM_SHEETS_ID
    )

def get_ddm_worksheet(sheet:ddm_settings.DDM_SHEET_NAMES) -> Spread:
    return sheets.get_google_worksheet(
        sheet_id=ddm_settings.DDM_SHEETS_ID,
        worksheet_name=sheet.value
    )

def ddm_sheet_to_df(
    sheet_name: ddm_settings.DDM_SHEET_NAMES,
    worksheet:Spread = None
) -> Tuple[pd.DataFrame, Spread]:
    """_summary_

    Args:
        sheet_name (ddm_settings.DDM_SHEET_NAMES): _description_

    Returns:
        Tuple[pd.DataFrame, Spread]: _description_
    """
    
    if worksheet:
        worksheet.open_sheet(sheet_name.value)
    else:
        worksheet = get_ddm_worksheet(sheet_name)
    
    raw_df = worksheet.sheet_to_df(index=0)

    formated_df = ddm_settings.format_DDM_dataframe(
        in_df=raw_df,
        sheet=sheet_name,
        format_mode='import'
    )

    return formated_df, worksheet


def df_to_ddm_sheet(
    df:pd.DataFrame,
    sheet: Spread,
    sheet_name: ddm_settings.DDM_SHEET_NAMES
):  
    formated_df = ddm_settings.format_DDM_dataframe(
        in_df=df,
        sheet=sheet_name,
        format_mode='export'
    )
    sheet.df_to_sheet(
        df=formated_df,
        index=False,
        sheet=sheet_name.value,
        replace=True

    )
    