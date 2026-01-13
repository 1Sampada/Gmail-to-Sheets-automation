# My Full Name: Sampada Kiran Parate
# Gmail to Google Sheets Automation

This project reads unread Gmail emails and stores them into Google Sheets using Python and OAuth 2.0.

## Steps
1. Connects to Gmail using OAuth
2. Fetches unread emails
3. Extracts sender, subject, date, and content
4. Appends data to Google Sheets
5. Prevents duplicate entries
6. Marks emails as read

## Duplicate Prevention
Each email has a unique Message ID.  
The script checks existing Message IDs in the sheet before inserting new rows.

## State Handling
Message IDs stored in Google Sheets act as state, ensuring emails are not reprocessed.

## Tech Used
- Python
- Gmail API
- Google Sheets API
- OAuth 2.0
