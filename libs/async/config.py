import os.path
import json


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth import compute_engine
import google.auth



# If modifying these scopes, delete the file token.json.

SCOPES = ['https://www.googleapis.com/auth/ediscovery',
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/devstorage.full_control',
        'https://www.googleapis.com/auth/devstorage.read_only',
        'https://www.googleapis.com/auth/devstorage.read_write',
        'https://www.googleapis.com/auth/admin.directory.orgunit',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/documents',
        'https://www.googleapis.com/auth/spreadsheets']
      


    
    
    
def authenticate() :

    
    creds = None
    
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('\\creds\\token.json'):
        creds = Credentials.from_authorized_user_file('\\creds\\token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '\\creds\\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('\\creds\\token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds



def ingest_config(config_name):

    
    # ingest the configuration file

    with open(config_name) as f:
        data = f.read()
  
      
    # reconstructing the data as a dictionary
    config = json.loads(data)
    

    return config
    
    
    
def get_default_project():

    project = google.auth.default()
    print("project=", project)

    return project
    
    
def get_credentials():

    credentials = compute_engine.Credentials()
    print("credentials=", credentials)
    
    return credentials