from google.cloud import bigquery

def create_external_table(project_id, bucket_name_destination, file_type, file_name, table_ref, dataset, folder_name, schemas_dict ):
  '''
  Function create an external table from files in GCS 


  Parameters:
    project_id(str): ID of the project 
    bucket_name_destination (str): Name of the bucket 
    file_type(str) : the type of the file
    file_name (str) : Name of the file
    table_ref (str) : Name of the table created
    dataset (str) : the dataset where the table is created
    schemas_dict (dict) : dict with fields as keys and types as values
  

  Returns:
    external table (bigquery.Table): created external table
  '''
  client = bigquery.Client(project_id)
  #Define your schema

  ls_schemas =[]
  for key,value in schemas_dict.items():
    schemafield = bigquery.schema.SchemaField(key,value)
    ls_schemas.append(schemafield)
  


  dataset_ref = client.dataset(dataset)
  table_ref = bigquery.TableReference(dataset_ref, table_ref )
  table = bigquery.Table(table_ref, ls_schemas)

  
  external_config = bigquery.ExternalConfig(file_type)
  source_uris = [f'gs://{bucket_name_destination}/{folder_name}/*/{file_name}'] #i.e for a csv file in a Cloud Storage bucket 
                                                #it would be something like "gs://<your-bucket>/<your-csv-file>"
  external_config.source_uris = source_uris
  file_type = file_type.upper()
  if file_type == 'CSV':
    external_config.options.field_delimiter = ","
    external_config.options.encoding = "UTF-8"
    external_config.options.skip_leading_rows = 1
  else : 
    raise NotImplementedError 

  table.external_data_configuration = external_config
  # external_config.options.quote_character 

  client.create_table(table)


