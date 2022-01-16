import json
import os
import re
from google.cloud import storage
import shlex
import subprocess

DBT_DOCS_BUCKET = os.environ.get('DBT_DOCS_BUCKET')
GCP_PROJECT = os.environ.get('FRONT_PROJECT_ID')
DBT_DOCS_READ_GROUP = os.environ.get('DBT_DOCS_READ_GROUP')
DBT_PROJECT_DIR = os.environ.get('DBT_PATH')

def get_dbt_populated_index(target_folder):

    print('Populating index.html ...')
    base_index_path = os.path.join(os.path.dirname(__file__), 'base_index.html')
    manifest_path = os.path.join(target_folder, 'manifest.json')
    catalog_path = os.path.join(target_folder, 'catalog.json')
    search_str = 'o=[i("manifest","manifest.json"+t),i("catalog","catalog.json"+t)]'

    with open(base_index_path, 'r') as f:
        content_index = f.read()

    with open(manifest_path, 'r') as f:
        json_manifest = json.loads(f.read())

    IGNORE_PROJECTS = [
        'dbt', 'dbt_bigquery', 'dbt_external_tables', 'dbt_utils', 
        'codegen'
    ]
    for element_type in ['nodes', 'sources', 'macros', 'parent_map', 'child_map']:  # navigate into manifest
        # We transform to list to not change dict size during iteration, we use default value {} to handle KeyError
        for key in list(json_manifest.get(element_type, {}).keys()):  
            for ignore_project in IGNORE_PROJECTS:
                if re.match(fr'^.*\.{ignore_project}\.', key):  # match with string that start with '*.<ignore_project>.'
                    del json_manifest[element_type][key]  # delete element

    with open(catalog_path, 'r') as f:
        json_catalog = json.loads(f.read())
        
    # Write manifest & catalog jsons in index.html
    new_str = "o=[{label: 'manifest', data: "+json.dumps(json_manifest)+"},{label: 'catalog', data: "+json.dumps(json_catalog)+"}]"
    new_content = content_index.replace(search_str, new_str)
    
    # Select "Database" tab by default & Hide "Project" tab
    # new_content = new_content.replace('{e.nav_selected="project"}', '{e.nav_selected="database"}')
    # new_content = new_content.replace('<div class="switch ">', '<div class="switch " hidden>')
    print('Successfully populated index.html')
    return new_content


def upload_populated_index(
    content,
    file_name='index.html'
):  
    
    print('Loading index.html to GCS ...')
    storage_client = storage.Client(project=GCP_PROJECT)
    bucket = storage_client.get_bucket(DBT_DOCS_BUCKET)
    blob = bucket.blob(file_name)
    blob.upload_from_string(content, content_type='text/html')
    print('Successfully loaded index.html to GCS')
   
    # Manage ACL
    acl = blob.acl
    acl.reload()
    acl.group(DBT_DOCS_READ_GROUP).grant_read()
    acl.save()
    blob.acl.save(acl=acl)
    print('Added ACL to index.html')


def run_subprocess(ls_commands, working_dir):
    """Run command provided as arg in path provided as arg

    Args:
        ls_commands (list): list of string representing the bash command to run
        working_dir (str): path when you want to change directory to before execution
        logger (logging.logger): (optional) for goblet `app.log`
    """
    out = ""
    err = ""
    
    try:
        process = subprocess.Popen(
            ls_commands,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            cwd=working_dir,
            env=os.environ.copy(),
            encoding='utf-8'
        )
        out, err = process.communicate()
        
        if process.returncode != 0:
            msg = f"{out}\n{err} failed"
            print(msg)
            return msg, False

    except Exception as e:
        raise e
    
    msg = out
    print(msg)
    return msg, True


def generate_dbt_docs():
    """
    Run `dbt docs generate`
    """
    ls_commands = [
        "dbt", "docs", "generate"
    ]
    print(f'Starting dbt docs generate ...')
    _, dbt_run_ok = run_subprocess(ls_commands, DBT_PROJECT_DIR)
    if dbt_run_ok:
        print(f'Successfully run dbt docs generate')
    else:
        print(f'Failed run dbt docs generate')


def run_dbt_debug():
    """
    Run `dbt debug `
    """
    ls_commands = [
        "dbt", "debug"
    ]
    print(f'Starting dbt debug ...')
    _, dbt_run_ok = run_subprocess(ls_commands, DBT_PROJECT_DIR)
    if dbt_run_ok:
        print(f'Successfully run dbt debug')
    else:
        print(f'Failed while trying to run dbt debug')


def run_dbt_deps():
    """
    Run `dbt debug `
    """
    ls_commands = [
        "dbt", "deps"
    ]
    print(f'Starting dbt deps  ...')
    _, dbt_run_ok = run_subprocess(ls_commands, DBT_PROJECT_DIR)
    if dbt_run_ok:
        print(f'Successfully run dbt deps')
    else:
        print(f'Failed while trying to run dbt deps')
