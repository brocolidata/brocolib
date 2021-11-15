import os
import shlex
import subprocess


def run_subprocess(ls_commands, working_dir, logger=None):
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
            env=os.environ.copy()
        )
        out, err = process.communicate()
        
        if process.returncode != 0:
            msg = f"{out}\n{err} failed"
            if logger:
                logger.error(msg)
            return msg

    except Exception as e:
        if logger:
            logger.error(str(e))
        return str(e)
    
    msg = f"{out}\n{err}"
    if logger:
        logger.info(msg)
    return msg


def run_dbt_model(sources, project_dir, logger=None):
    """Run `dbt run` and select child of sources provided as arg
    using `"--select source:stg.SOURCE+`
    See [Using Unions Set Operators for Node Selection](https://docs.getdbt.com/reference/node-selection/set-operators#unions)

    Args:
        sources (list): all sources that are parent of the branches that will be run
        project_dir (str): path to the dbt project
        logger (logging.logger): (optional) for goblet `app.log`
    """
    ls_commands = [
        "dbt", "run",
        "--select"
    ]
    ls_commands += [f"source:stg.{source}+" for source in sources]
    logger.info('START dbt run for', ','.join(sources))
    _ = run_subprocess(ls_commands, project_dir, logger)
    logger.info('END dbt run for', ','.join(sources))

def stage_table(sources, project_dir, logger=None):
    """stage tables from datalake to staging layer in dwh

    Args:
        sources (list): list of tables to stage
        project_dir (str): path to the dbt project
        logger (logging.logger): (optional) for goblet `app.log`
    """
    for source in sources:
        ls_commands = [
            "dbt", 
            "run-operation", 
            "stage_external_sources",
        ]
        ls_commands += shlex.split(f"--args \"select: stg.{source}\"")
        logger.info('START staging', source)
        _ = run_subprocess(ls_commands, project_dir, logger)
        logger.info('END staging', source)
