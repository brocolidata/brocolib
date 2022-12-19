# from oauth2client.service_account import ServiceAccountCredentials
import time
import requests
from google.auth import jwt
from google.oauth2 import service_account
import os
import json
from google.auth import crypt

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')


def get_credential_file_path() -> str:
    return os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


def get_jwt_signer() -> crypt.RSASigner:
    return crypt.Signer(get_private_key())


def get_creds(scopes:list) -> service_account.Credentials:
    creds = service_account.Credentials.from_service_account_file(
        filename=get_credential_file_path(), 
        scopes=scopes
    )
    return creds


def get_credential_file_asdict():
    with open(get_credential_file_path()) as f:
        cred_json = json.load(f)
    return cred_json
    
def get_key_from_credential_file(key_to_get: str) -> str:
    with open(get_credential_file_path()) as f:
        cred_json = json.load(f)
    return cred_json.get(key_to_get)


def get_private_key() -> str:
    return get_key_from_credential_file('private_key')


def get_client_email() -> str:
    return get_key_from_credential_file('client_email')


def get_jwt_token(scopes:list):
    client_email = get_client_email()
    iat = int(time.time())
    exp = iat + 3600
    header = {'alg': 'RS256'}
    claim_set = {
        "iss": client_email,
        #  "sub": "test@leanscale.com",
        "sub": client_email,
        #  "email": "test@leanscale.com",
        "email": client_email,
        "scope": " ".join(scopes),
        "aud": "https://oauth2.googleapis.com/token",
        "exp": exp, 
        "iat": iat
    }

    # s = jwt.encode(header, claim_set, get_private_key())
    s = jwt.encode(
        signer=get_jwt_signer(),
        payload=claim_set,
        header=header,
        key_id=get_private_key()
    )
    r = requests.post("https://oauth2.googleapis.com/token",
            params={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": s
        })
    
    # Right now you are getting an access token for each time.
    # If you put this code into a server, you have to control
    # your token expiration before creating a new token.
    return r.json()['access_token']
        
def get_jwt_header(scopes:list):
    token = get_jwt_token(scopes)
    return {
        "Authorization": f"Bearer {token}",
    }