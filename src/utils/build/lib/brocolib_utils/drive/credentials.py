from oauth2client.service_account import ServiceAccountCredentials
import os

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
SCOPE = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

def get_creds():

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_APPLICATION_CREDENTIALS, SCOPE)
    
    return creds