import os
import shlex
import subprocess


def run_subprocess(ls_commands: list, working_dir: str, logger=None):
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
            if logger:
                logger.error(msg)
            return msg, False

    except Exception as e:
        if logger:
            logger.error(str(e))
        return str(e), False
    
    msg = out
    if logger:
        logger.info(msg)
    return msg, True


def run_dbt_model(sources: list, project_dir: str, logger=None):
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
    logger.info(f'START dbt run for {str(sources)}')
    _, dbt_run_ok = run_subprocess(ls_commands, project_dir, logger)
    if dbt_run_ok:
        logger.info(f'END dbt run successful for {str(sources)}')
    else:
        logger.error(f'END dbt run failed for {str(sources)}')


def stage_table(sources: list, project_dir: str, logger=None):
    """stage tables from datalake to staging layer in dwh

    Args:
        sources (list): list of tables to stage
        project_dir (str): path to the dbt project
        logger (logging.logger): (optional) for goblet `app.log`
    """
    staging_successful = True
    for source in sources:
        ls_commands = [
            "dbt", 
            "run-operation", 
            "stage_external_sources",
        ]
        ls_commands += shlex.split(f"--args \"select: stg.{source}\"")
        ls_commands += shlex.split(f"--vars \"ext_full_refresh: true\"")
        logger.info(f'START staging {source}')
        _, sources_are_staged = run_subprocess(ls_commands, project_dir, logger)
        if sources_are_staged:
            logger.info(f'END staging successful for {source}')
        else:
            logger.error(f'END staging successful for {source}')
            staging_successful = False
    if staging_successful:
        return True
    else:
        return False
