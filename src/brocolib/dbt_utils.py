import subprocess


def run_dbt_model(models, project_dir, profiles_dir):
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
        "--select"
    ]
    ls_commands += [f"source:stg.{model}+" for model in models]
    output = run_subprocess(ls_commands)
    return output


def stage_table(sources, project_dir, profiles_dir, logger):
    """stage tables from datalake to staging layer in dwh
        and returns log

    Args:
        sources (list): list of tables to stage
        project_dir (str): path to the dbt project_dir
        profiles_dir (str): path to the dbt profiles_dir

    Returns:
        output (bytes): log of the staging
    """
    for source in sources:
        ls_commands = [
            "dbt", "run-operation",
            "stage_external_sources", 
            "--project-dir", project_dir,
            "--profiles-dir", profiles_dir,
            "--args", f"'select: stg.{source}'"
        ]

        output = run_subprocess(ls_commands)
        logger.info(f"staging output for {source} :")
        logger.info(output)


def run_subprocess(ls_commands):
    """run command provided as arg and returns output

    Args:
        ls_commands (list): list of string representing the bash command to run

    Returns:
        (bytes): output of the bash command
    """
    out = ""
    err = ""
    
    try:
        process = subprocess.Popen(
            ls_commands,
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