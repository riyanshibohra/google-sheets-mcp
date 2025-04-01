# src/datacraft/tools/fetch_sheet.py
import gspread
import pandas as pd
import os
from google.oauth2.service_account import Credentials

def fetch_sheet(sheet_url: str, tab_name: str) -> pd.DataFrame:
    """Fetch data from a Google Sheet and convert it to a DataFrame."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(current_dir, 'credentials.json')
    
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Credentials file not found at: {credentials_path}")
    
    creds = Credentials.from_service_account_file(
        credentials_path, 
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.worksheet(tab_name)
    return pd.DataFrame(worksheet.get_all_records())

def update_sheet(sheet_url: str, tab_name: str, df: pd.DataFrame) -> bool:
    """Update a Google Sheet with data from a DataFrame."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(current_dir, 'credentials.json')
    
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Credentials file not found at: {credentials_path}")
    
    creds = Credentials.from_service_account_file(
        credentials_path, 
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    client = gspread.authorize(creds)
    
    # Update the sheet
    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.worksheet(tab_name)
    worksheet.clear()
    worksheet.update('A1', [df.columns.tolist()] + df.values.tolist())
    
    return True
