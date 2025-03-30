# src/datacraft/tools/fetch_sheet.py
import gspread
import pandas as pd
import json
from google.oauth2.service_account import Credentials

def fetch_sheet(sheet_url: str, tab_name: str) -> str:
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.worksheet(tab_name)
    data = worksheet.get_all_records()

    df = pd.DataFrame(data)
    return df.to_json(orient='split')

