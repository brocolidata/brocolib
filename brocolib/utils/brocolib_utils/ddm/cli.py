import typer
from typing import Optional

from brocolib_utils.ddm import sources_parser

app = typer.Typer()

@app.callback()
def ddm():
    """
    Domain Data Management Sheets Parser & Generator
    """


@app.command()
def fill_sources(
    source_name: Optional[str] = typer.Argument(None, help="dbt source name"),
    datalake_bucket: Optional[str] = typer.Argument(None, help="datalake bucket name where the data is located")
):
    """
    Filling Source Tables & Source Columns worksheets in the DDM Google Sheets
    """
    source_name = source_name or typer.prompt("Name of the source ?")

    if not source_name:
        typer.echo('You must provide a source_name. Exiting.')
        raise typer.Exit(code=1)
    
    typer.echo(f"Filling source sheets for : {source_name} ..")

    sources_parser.fill_sources_sheets(
        source_name=source_name, 
        datalake_bucket=datalake_bucket
    )

    typer.echo(f"Done filling {source_name}!")
    


# if __name__ == "__main__":
#     app()