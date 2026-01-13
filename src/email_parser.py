import base64


def get_header(headers, name):
    """
    Helper function to extract a specific header value
    """
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    return ""


def extract_email_body(payload):
    """
    Extract plain text email body from Gmail payload
    """
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8')
    else:
        data = payload['body'].get('data')
        if data:
            return base64.urlsafe_b64decode(data).decode('utf-8')

    return ""
