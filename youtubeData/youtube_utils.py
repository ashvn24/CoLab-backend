# youtube_utils.py
import os
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from backend.settings import CLIENT_SECRET_FILE_PATH

CLIENT_SECRETS_FILE = CLIENT_SECRET_FILE_PATH
API_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service(credentials_path):
    creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=80)   #443 for https

        with open(credentials_path, 'w') as token:
            token.write(creds.to_json())

    return build(API_NAME, API_VERSION, credentials=creds)


