"""Handles Google Sheets API authentication and connection."""

import gspread
from google.oauth2.service_account import Credentials

_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]


def get_worksheet(credentials_path: str, sheet_id: str, worksheet_name: str) -> gspread.Worksheet:
    """Authenticates with Google and returns the target worksheet."""
    credentials = Credentials.from_service_account_file(credentials_path, scopes=_SCOPES)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(sheet_id)
    return spreadsheet.worksheet(worksheet_name)
