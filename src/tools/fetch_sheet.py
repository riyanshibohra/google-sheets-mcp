# src/datacraft/tools/fetch_sheet.py
import gspread
import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials

def fetch_sheet(sheet_url: str, tab_name: str) -> str:
    scopes = ['https://www.googleapis.com/auth/spreadsheets']  # Full access scope
    current_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(current_dir, 'credentials.json')
    print(f"Using credentials from: {credentials_path}")
    print(f"File exists: {os.path.exists(credentials_path)}")
    
    creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.worksheet(tab_name)
    data = worksheet.get_all_records()

    df = pd.DataFrame(data)
    return df.to_json(orient='split')

def update_sheet(sheet_url: str, tab_name: str, df_json: str) -> bool:
    """Update the Google Sheet with modified data"""
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    current_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(current_dir, 'credentials.json')
    
    # Clean the JSON string
    df_json = df_json.replace('\\', '')
    if df_json.startswith('"') and df_json.endswith('"'):
        df_json = df_json[1:-1]
    
    creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
    client = gspread.authorize(creds)

    df = pd.read_json(df_json, orient='split')
        
        # Convert DataFrame to list of lists (including headers)
    headers = df.columns.tolist()
    values = df.values.tolist()
    all_values = [headers] + values

    # Update the sheet
    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.worksheet(tab_name)
        
    # Clear existing content and update with new data
    worksheet.clear()
    worksheet.update('A1', all_values)
        
    return True


