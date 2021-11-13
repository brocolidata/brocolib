# import subprocess


# def run_dbt_model(model, project_dir, profiles_dir):
#     """run dbt model provided as arg and return run log

#     Args:
#         model (str): dbt model name
#         project_dir (str): path to the dbt project_dir
#         profiles_dir (str): path to the dbt profiles_dir

#     Returns:
#         output (str): log of the dbt run
#     """
#     ls_commands = [
#         "dbt", "run", 
#         "--project-dir", project_dir,
#         "--profiles-dir", profiles_dir    
#     ]
#     ls_commands.extend(["--models", f"+{model}+"])
#     output = subprocess.run(ls_commands, stdout=subprocess.PIPE)
#     return output


import subprocess
import sys


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
        "--profiles-dir", profiles_dir,
        "--models", f"+{model}+"
    ]
    # ls_commands.extend(["--models", f"+{model}+"])
    # output = subprocess.run(ls_commands, stdout=subprocess.PIPE)
    output = run_subprocess(ls_commands)
    return output


def run_subprocess(ls_commands):
    out = ""
    err = ""
    ls_executable = [sys.executable, ls_commands]
    
    try:
        process = subprocess.Popen(
            ls_executable,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        out, err = process.communicate()
        
        if process.returncode != 0:
            return f"{out}\n{err} failed"

    except Exception as e:
        return str(e)

    return f"{out}\n{err}"