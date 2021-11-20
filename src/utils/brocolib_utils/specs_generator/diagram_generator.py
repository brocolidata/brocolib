# importing the required libraries
import diagrams as diag
from diagrams.custom import Custom
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build

from brocolib_utils.drive import get_creds
from brocolib_utils.drive import sheet_to_df, clean_columns_name, get_sheet_title, explode_sources
from brocolib_utils.settings import DBT_MODELS_SHEET_NAME

TABLE_ICON_FILE_PATH = "/brocolib_dbt/brocolib/specs_generator/database_table_icon.jpeg"

def get_next_nodes(node_name, dataframe, dc_models_icon):
    ls_next_nodes = []
    filter_node = (dataframe.model_source == node_name)
    df_filtered = dataframe[filter_node]
    for model in df_filtered.model_name.unique():
        ls_next_nodes.append(dc_models_icon[model])
    return ls_next_nodes

def generate_diagram(sheet_url, diagram_name=None, directory="."):
    
    dataframe = sheet_to_df(
        sheet_url=sheet_url,
        sheet_name=DBT_MODELS_SHEET_NAME
    )
    if diagram_name is None:
        diagram_name = get_sheet_title(sheet_url)
    dataframe = clean_columns_name(dataframe)
    diagram = diag.Diagram(diagram_name, show=False, filename=f"{directory}/{diagram_name}", direction="LR")
    with diagram:
        dc_models_icon = {}
        for layer in dataframe.layer.unique():
            filter_layer = (dataframe.layer==layer)
            df_filtered_layer = dataframe[filter_layer]
            cluster = diag.Cluster(layer)
            with cluster:
                for model in df_filtered_layer.itertuples():
                    dc_models_icon[model.model_name] = Custom(model.model_name, TABLE_ICON_FILE_PATH)

        for node in dc_models_icon:
            dataframe = explode_sources(dataframe)
            next_nodes = get_next_nodes(node, dataframe, dc_models_icon)
            if len(next_nodes)>0:
                dc_models_icon[node] - next_nodes
    print(f'saving file to {directory}/{diagram_name}.png')
    return diagram, f"{directory}/{diagram_name}.png"
                

def send_image_to_drive(project_drive_folder_id, file_path ,output_file_name="database_specs.png"):
    service = build('drive', 'v3')
    print("project_drive_folder_id")
    print(project_drive_folder_id)
    file_metadata = {
        'name': output_file_name,
        'parents': [project_drive_folder_id]
    }
    media = MediaFileUpload(file_path, mimetype="image/png")
    file_created = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('Specs image successfully sent to Google Drive !')
  