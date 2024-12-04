from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.labels'
          ]

def get_credentials():
    creds = None
    # Check if the token.json file exists, which stores the user's access and refresh tokens.
    # This file is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        # Load the credentials from the token.json file.
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no valid credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        # If the credentials are expired but a refresh token is available, attempt to refresh them.
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())  # Refresh the credentials using the Request object.
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                # If refreshing fails, delete the token.json file to force re-authentication.
                os.remove('token.json')
                # Create a flow object to handle the OAuth 2.0 authorization.
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json', SCOPES)
                # Run the local server to complete the authorization process.
                creds = flow.run_local_server(port=0)
        else:
            # If no valid credentials are available, initiate the authorization flow.
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)  # Run the local server for user login.
        
        # Save the credentials for the next run to avoid re-authentication.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())  # Write the credentials to token.json.
    
    return creds  # Return the valid credentials.

def get_service():
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    return service