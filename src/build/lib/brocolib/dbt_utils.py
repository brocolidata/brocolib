import subprocess


def run_dbt_model(model, project_dir, profiles_dir):
    """run dbt model provided as arg and return run log

    Args:
        model (str): dbt model name
        project_dir (str): path to the dbt project_dir
        profiles_dir (str): path to the dbt profiles_dir

    Returns:
        output (str): log of the dbt run
    """
    ls_commands = [
        "dbt", "run", 
        "--project-dir", project_dir,
        "--profiles-dir", profiles_dir    
    ]
    ls_commands.extend(["--models", f"+{model}+"])
    output = subprocess.run(ls_commands, stdout=subprocess.PIPE)
    return output