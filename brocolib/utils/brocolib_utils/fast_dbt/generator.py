from collections import OrderedDict
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString 
from brocolib_utils.settings import (TABLE_NAME_COL)

def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')


# define a custom representer for strings
class quoted(str):
    pass


def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')


def get_loaded_sources(dataframe):
    ls_loaded = []
    for table in dataframe.itertuples():
        if table.EL != "":
            ls_loaded.append(getattr(table, TABLE_NAME_COL))     
    return ls_loaded


def init_dbt_sources(database, loader=None, version=2):
    # dc_dbt_sources = OrderedDict()
    dc_dbt_sources = {}
    dc_dbt_sources["version"]=version
    dc_dbt_sources["sources"]=[]
    
    # for source in getattr(sources_dataframe, SOURCE_DATASET_COL).unique():
        # dc_source = OrderedDict()
    dc_source = {}
    dc_source["name"] = "stg"
    dc_source["database"] = database
    dc_source["loader"] = "gcloud storage"
    dc_source["tables"] = []

    dc_dbt_sources["sources"].append(dict(dc_source))
    
    return dc_dbt_sources




def dict_to_yaml(yaml_dict, yaml_file_path="./stg.yml"):
    yaml=YAML()
    yaml.default_flow_style = False
    with open(yaml_file_path, 'w') as file:
        yaml.dump(yaml_dict, file)
