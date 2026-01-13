import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Gmail API scope (read-only)
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets'
]

def get_gmail_service():
    """
    Handles OAuth authentication and returns Gmail API service
    """
    creds = None

    # Load existing token if present
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If token is invalid or missing, login again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json',
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Create Gmail service
    service = build('gmail', 'v1', credentials=creds)
    return service


def get_unread_emails(service):
    """
    Fetch unread inbox emails
    """
    results = service.users().messages().list(
        userId='me',
        q='is:unread in:inbox'
    ).execute()

    return results.get('messages', [])

def mark_as_read(service, msg_id):
    """
    Marks an email as read by removing UNREAD label
    """
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()
