# src/datacraft/server.py

from mcp.server.fastmcp import FastMCP
from tools.fetch_sheet import fetch_sheet
from tools.clean_data import clean_data

mcp = FastMCP("DataCraft")

# Tool 1: Fetch Google Sheet data
@mcp.tool()
def fetch_google_sheet(sheet_url: str, tab_name: str) -> str:
    return fetch_sheet(sheet_url, tab_name)

# Tool 2: Clean missing data
@mcp.tool()
def clean_missing_data(df_json: str, method: str = "mean") -> str:
    return clean_data(df_json, method)

if __name__ == "__main__":
    mcp.run()