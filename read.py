from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError


def read_sheets(service_account_file, spreadsheet_id, sheet_number, error_callback=None):
    range_name = f"Sheet{sheet_number}"
    creds = Credentials.from_service_account_file(
        service_account_file,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])

    service = build('sheets', 'v4', credentials=creds)

    try:
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])

        data = []

        if not values:
            if error_callback:
                error_callback(f"No data found, check your settings")
        else:
            # Assuming the first row contains the headers
            headers = values[0]
            data = []
            for row in values[1:]:
                # Fill missing cells with None
                row_data = [(cell if cell != '' else None) for cell in row]
                # Pad row_data if it's shorter than headers
                row_data += [None] * (len(headers) - len(row_data))
                data.append(dict(zip(headers, row_data)))

        print(data)
        return data

    except RefreshError as e:
        # Handle the RefreshError specifically
        if error_callback:
            error_callback(f"Authentication failed, check your system time")
        print(f"Authentication failed: {e}")
        return []

    except HttpError as e:
        # Invoke the error callback with the error message
        if error_callback:
            error_callback(f"Failed to read sheet, check your settings")
        print(e)
        return []
