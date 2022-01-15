import json
import os
from google.cloud import storage
import shlex
import subprocess


def get_dbt_populated_index(target_folder):

    print('Populating index.html ...')
    index_path = os.path.join(target_folder, 'index.html')
    manifest_path = os.path.join(target_folder, 'manifest.json')
    catalog_path = os.path.join(target_folder, 'catalog.json')
    search_str = 'o=[i("manifest","manifest.json"+t),i("catalog","catalog.json"+t)]'

    with open(index_path, 'r') as f:
        content_index = f.read()
        
    with open(manifest_path, 'r') as f:
        json_manifest = json.loads(f.read())

    with open(catalog_path, 'r') as f:
        json_catalog = json.loads(f.read())
        
    # with open('./index2.html', 'w') as f:
    new_str = "o=[{label: 'manifest', data: "+json.dumps(json_manifest)+"},{label: 'catalog', data: "+json.dumps(json_catalog)+"}]"
    new_content = content_index.replace(search_str, new_str)
    print('Successfully populated index.html')
    return new_content


def upload_populated_index(
    content,
    file_name='index.html'
):  
    bucket = os.environ.get('DBT_DOCS_BUCKET')
    gcp_project = os.environ.get('FRONT_PROJECT_ID')
    read_group = os.environ.get('DBT_DOCS_READ_GROUP')

    print('Loading index.html to GCS ...')
    storage_client = storage.Client(project=gcp_project)
    bucket = storage_client.get_bucket(bucket)
    blob = bucket.blob(file_name)
    blob.upload_from_string(content, content_type='text/html')
    print('Successfully loaded index.html to GCS')
   
    # Manage ACL
    acl = blob.acl
    acl.reload()
    acl.group(read_group).grant_read()
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
    project_dir = os.environ.get('DBT_PATH')
    print(f'Starting dbt docs generate ...')
    _, dbt_run_ok = run_subprocess(ls_commands, project_dir)
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
    project_dir = os.environ.get('DBT_PATH')
    print(f'Starting dbt debug ...')
    _, dbt_run_ok = run_subprocess(ls_commands, project_dir)
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
    project_dir = os.environ.get('DBT_PATH')
    print(f'Starting dbt deps  ...')
    _, dbt_run_ok = run_subprocess(ls_commands, project_dir)
    if dbt_run_ok:
        print(f'Successfully run dbt deps')
    else:
        print(f'Failed while trying to run dbt deps')
