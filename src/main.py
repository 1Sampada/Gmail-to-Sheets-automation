from gmail_service import (
    get_gmail_service,
    get_unread_emails,
    mark_as_read
)
from email_parser import get_header, extract_email_body
from sheets_service import (
    get_sheets_service,
    get_existing_message_ids,
    append_row
)
from config import SPREADSHEET_ID, SHEET_NAME


if __name__ == "__main__":
    # Gmail auth
    gmail_service = get_gmail_service()
    creds = gmail_service._http.credentials

    # Sheets auth
    sheets_service = get_sheets_service(creds)

    # Existing message IDs (state)
    existing_ids = get_existing_message_ids(
        sheets_service,
        SPREADSHEET_ID,
        SHEET_NAME
    )

    messages = get_unread_emails(gmail_service)

    for msg in messages:
        msg_id = msg['id']

        # Duplicate check
        if msg_id in existing_ids:
            continue

        message = gmail_service.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'
        ).execute()

        headers = message['payload']['headers']
        payload = message['payload']

        sender = get_header(headers, 'From')
        subject = get_header(headers, 'Subject')
        date = get_header(headers, 'Date')
        body = extract_email_body(payload)

        row = [sender, subject, date, body, msg_id]

        append_row(
            sheets_service,
            SPREADSHEET_ID,
            SHEET_NAME,
            row
        )

        # Mark email as read
        mark_as_read(gmail_service, msg_id)

    print("Processing complete.")
