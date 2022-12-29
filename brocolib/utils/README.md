# brocolib_utils

- `fast_dbt` : Generate dbt manifests files based on Domain Data Management Google Sheets
- `ddm` : Domain Data Management Google Sheets content management
- `catalog_gen` : Generate Data Catalog based on dbt

## Installation 

Find the latest version `brocolib-utils` in [Release](https://github.com/brocolidata/brocolib/releases) and get the URL of the `.whl` artifact related to the Release. 

## Environment variables

| **Variable Name**              | **Description**                                    |
|--------------------------------|----------------------------------------------------|
| BACK_PROJECT_ID                | ID of the `back-` GCP project                      |
| DATALAKE_BUCKET                | Name of the GCS Bucket used as DataLake            |
| GOOGLE_APPLICATION_CREDENTIALS | Path to Service Account file                       |
| DDM_SHEETS_ID                  | ID of the DDM Google Sheets                        |
| DBT_DOCS_BUCKET                | Name of the Data Catalog GCS Bucket                |
| FRONT_PROJECT_ID               | ID of the `front-` GCP project                     |
| DBT_DOCS_READ_GROUP            | Google Groups with READ rights on the Data Catalog |
| DBT_PATH                       | Path to the dbt project                            |