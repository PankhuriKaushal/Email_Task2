import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Set the API scope and credentials file path
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDS_FILE = 'path/to/your/credentials.json'

def get_gmail_service():
    """Get Gmail API service."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def list_last_200_emails():
    """List the last 200 emails."""
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', maxResults=200).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
    else:
        print('Sender\t\t\tSubject')
        print('---------------------------------------------')
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            headers = msg['payload']['headers']
            sender = [header['value'] for header in headers if header['name'] == 'From'][0]
            subject = [header['value'] for header in headers if header['name'] == 'Subject'][0]
            print(f'{sender}\t{subject}')

if _name_ == '_main_':
    list_last_200_emails()