# src/datacraft/server.py

import os
import json
from typing import Optional, Dict, List, Any
from pathlib import Path

import gspread
from fastapi import FastAPI, HTTPException
from google.oauth2.service_account import Credentials
from google.oauth2.credentials import Credentials as OAuthCredentials
from pydantic import BaseModel
from mcp import MCPRouter, MCPRequest

# Initialize FastAPI app
app = FastAPI()
router = MCPRouter()

# Constants
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

class GoogleSheetsClient:
    def __init__(self):
        self.client = None
        self.folder_id = os.getenv('DRIVE_FOLDER_ID')
        
    async def initialize(self):
        """Initialize the Google Sheets client with appropriate credentials."""
        if self.client:
            return

        # Try service account first
        service_account_path = os.getenv('SERVICE_ACCOUNT_PATH')
        if service_account_path and Path(service_account_path).exists():
            credentials = Credentials.from_service_account_file(
                service_account_path,
                scopes=SCOPES
            )
            self.client = gspread.authorize(credentials)
            return

        # Fall back to OAuth
        credentials_path = os.getenv('CREDENTIALS_PATH', 'credentials.json')
        token_path = os.getenv('TOKEN_PATH', 'token.json')
        
        if not Path(credentials_path).exists():
            raise HTTPException(status_code=500, detail="No credentials found")
            
        if Path(token_path).exists():
            with open(token_path) as token:
                credentials = OAuthCredentials.from_authorized_user_info(
                    json.load(token),
                    SCOPES
                )
        else:
            # Handle OAuth flow
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            credentials = flow.run_local_server(port=0)
            
            # Save the credentials
            with open(token_path, 'w') as token:
                token.write(credentials.to_json())

        self.client = gspread.authorize(credentials)

# Initialize global client
sheets_client = GoogleSheetsClient()

@router.on_startup
async def startup():
    """Initialize the Google Sheets client on startup."""
    await sheets_client.initialize()

@router.function("fetch_google_sheet")
async def fetch_google_sheet(request: MCPRequest) -> Dict[str, Any]:
    """Fetch data from a Google Sheet."""
    sheet_url = request.arguments.get("sheet_url")
    tab_name = request.arguments.get("tab_name")
    
    try:
        # Open the spreadsheet
        spreadsheet = sheets_client.client.open_by_url(sheet_url)
        worksheet = spreadsheet.worksheet(tab_name)
        
        # Get all values
        data = worksheet.get_all_records()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.function("update_google_sheet")
async def update_google_sheet(request: MCPRequest) -> Dict[str, Any]:
    """Update data in a Google Sheet."""
    sheet_url = request.arguments.get("sheet_url")
    tab_name = request.arguments.get("tab_name")
    df_json = request.arguments.get("df_json")
    
    try:
        # Parse the JSON data
        data = json.loads(df_json)
        
        # Open the spreadsheet
        spreadsheet = sheets_client.client.open_by_url(sheet_url)
        worksheet = spreadsheet.worksheet(tab_name)
        
        # Clear existing data and update
        worksheet.clear()
        if data:
            worksheet.update([list(data[0].keys())] + [list(row.values()) for row in data])
        
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.function("add_row")
async def add_row(request: MCPRequest) -> Dict[str, Any]:
    """Add a new row to the Google Sheet."""
    sheet_url = request.arguments.get("sheet_url")
    tab_name = request.arguments.get("tab_name")
    row_data = request.arguments.get("row_data")
    
    try:
        # Open the spreadsheet
        spreadsheet = sheets_client.client.open_by_url(sheet_url)
        worksheet = spreadsheet.worksheet(tab_name)
        
        # Add the row
        worksheet.append_row(list(row_data.values()))
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.function("edit_row")
async def edit_row(request: MCPRequest) -> Dict[str, Any]:
    """Edit an existing row in the Google Sheet."""
    sheet_url = request.arguments.get("sheet_url")
    tab_name = request.arguments.get("tab_name")
    row_identifier = request.arguments.get("row_identifier")
    updated_data = request.arguments.get("updated_data")
    
    try:
        # Open the spreadsheet
        spreadsheet = sheets_client.client.open_by_url(sheet_url)
        worksheet = spreadsheet.worksheet(tab_name)
        
        # Find the row
        data = worksheet.get_all_records()
        for idx, row in enumerate(data):
            if all(row.get(k) == v for k, v in row_identifier.items()):
                # Update the row
                cell_list = worksheet.range(f'A{idx+2}:Z{idx+2}')
                for i, value in enumerate(updated_data.values()):
                    cell_list[i].value = value
                worksheet.update_cells(cell_list)
                return {"status": "success"}
                
        return {"status": "error", "message": "Row not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.function("delete_row")
async def delete_row(request: MCPRequest) -> Dict[str, Any]:
    """Delete a row from the Google Sheet."""
    sheet_url = request.arguments.get("sheet_url")
    tab_name = request.arguments.get("tab_name")
    row_identifier = request.arguments.get("row_identifier")
    
    try:
        # Open the spreadsheet
        spreadsheet = sheets_client.client.open_by_url(sheet_url)
        worksheet = spreadsheet.worksheet(tab_name)
        
        # Find and delete the row
        data = worksheet.get_all_records()
        for idx, row in enumerate(data):
            if all(row.get(k) == v for k, v in row_identifier.items()):
                worksheet.delete_rows(idx + 2)  # +2 because of header and 1-based indexing
                return {"status": "success"}
                
        return {"status": "error", "message": "Row not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Add router to app
app.include_router(router)

def main():
    """Entry point for the application."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()