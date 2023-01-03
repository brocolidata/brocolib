import os
import pathlib
from brocolib_utils.catalog_gen import dbt_catalog

DBT_TARGET_FOLDER = "dbt_target"
DATA_CATALOG_HTML_FOLDER = "data_catalog_html"

def test_get_dbt_populated_index():
    parent_dir = pathlib.Path(__file__).parent.resolve()
    full_target_path = os.path.join(parent_dir, DBT_TARGET_FOLDER)
    content = dbt_catalog.get_dbt_populated_index(
        target_folder=full_target_path
    )
    
    full_index_path = os.path.join(parent_dir, DATA_CATALOG_HTML_FOLDER, 'index.html')
    with open(full_index_path) as f:
        test_content = f.read()
    assert content == test_content