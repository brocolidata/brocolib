from google.cloud import storage
from brocolib_utils import settings
from typing import Literal

STORAGE_CLASSES = Literal["STANDARD", "NEARLINE", "COLDLINE", "ARCHIVE"]
DEFAULT_STORAGE_CLASS = "STANDARD"

def get_storage_client(project:str=None):
    project = project or settings.DATALAKE_PROJECT
    return storage.Client(project=project)


def create_bucket(
    bucket_name:str,
    bucket_location:str=None,
    project:str=None,
    storage_class:STORAGE_CLASSES=None
):
    storage_client = get_storage_client(project=project)
    bucket = storage_client.bucket(bucket_name)
    bucket_exists = bucket.exists()
    if not bucket_exists:
        bucket.storage_class = storage_class or DEFAULT_STORAGE_CLASS
        bucket = storage_client.create_bucket(bucket, location=bucket_location)
    return bucket, bucket_exists


def delete_bucket(bucket_name:str, project:str = None):
    storage_client = get_storage_client(project)
    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()