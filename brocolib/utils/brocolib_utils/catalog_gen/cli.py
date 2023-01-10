import typer
from typing import Optional
from pathlib import Path
from brocolib_utils.catalog_gen.dbt_catalog import (generate_dbt_docs, get_dbt_populated_index, 
    run_dbt_debug, run_dbt_deps, upload_populated_index)

app = typer.Typer()

@app.callback()
def data_catalog():
    """
    Domain Data Management Sheets Parser & Generator
    """


@app.command()
def deploy(
    target_path: Optional[Path] = typer.Option(Path('/tmp/target'), help="dbt target path"),
    is_CI: bool = typer.Option(False, help="set to True for CI"),
    debug: bool = typer.Option(False, help="run dbt debug before deployment")
):
    """
    Generate & Deploy Data Catalog to a Google Cloud Storage bucket
    """
    if is_CI:
        run_dbt_deps()

    if debug:
        run_dbt_debug()

    generate_dbt_docs()

    new_content = get_dbt_populated_index(
        target_folder=target_path
    )

    upload_populated_index(
        content=new_content
    )
