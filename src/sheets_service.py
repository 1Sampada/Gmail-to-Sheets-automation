from googleapiclient.discovery import build


def get_sheets_service(creds):
    return build('sheets', 'v4', credentials=creds)


def get_existing_message_ids(service, spreadsheet_id, sheet_name):
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!E:E"
    ).execute()

    values = result.get('values', [])
    return set(row[0] for row in values if row)



def append_row(service, spreadsheet_id, sheet_name, row):
    body = {
        'values': [row]
    }

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=sheet_name,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
