import os
import pickle
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def read_last_email(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
        return

    message = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
    
    email_data = message['payload']['headers']
    for values in email_data:
        name = values['name']
        if name == 'From':
            from_name = values['value']
        if name == 'Subject':
            subject = values['value']

    print(f"From: {from_name}")
    print(f"Subject: {subject}")
    
    if 'parts' in message['payload']:
        for part in message['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                body = part['body']['data']
                print("Body:")
                print(body)
    else:
        body = message['payload']['body']['data']
        print("Body:")
        print(body)

if __name__ == '__main__':
    service = get_gmail_service()
    read_last_email(service)