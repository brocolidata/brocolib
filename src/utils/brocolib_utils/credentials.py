# from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import os
import json
from google.auth import crypt

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')


def get_credential_file_path() -> str:
    return os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


def get_jwt_signer() -> crypt.RSASigner:
    # return crypt.Signer(get_private_key())
    return crypt.RSASigner.from_service_account_file(get_credential_file_path())


# def get_creds(scopes):
#     # add credentials to the account
#     creds = ServiceAccountCredentials.from_json_keyfile_name(
#         filename=get_credential_file_path(), 
#         scopes=scopes
#     )
#     return creds


def get_creds(scopes) -> Credentials:
    # add credentials to the account
    creds = Credentials.from_service_account_file(
        filename=get_credential_file_path(), 
        scopes=scopes
    )
    return creds


def get_key_from_credential_file(key_to_get: str) -> str:
    with open(get_credential_file_path()) as f:
        cred_json = json.load(f)
    return cred_json.get(key_to_get)


def get_private_key() -> str:
    return get_key_from_credential_file('private_key')


def get_client_email() -> str:
    return get_key_from_credential_file('client_email')

    
def scope(scopes: list) -> str:
    # scope_str = ""
    # for api in scopes:
    #     scope_str += api + " "
    # return scope_str
    return " ".join(scopes)