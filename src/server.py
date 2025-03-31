# src/server.py

from mcp.server.fastmcp import FastMCP
from tools.fetch_sheet import fetch_sheet, update_sheet
from tools.data_operations import add_data, edit_data, delete_data
from tools.column_operations import add_column, rename_column, transform_column
from typing import Dict, List, Any
import pandas as pd
import os

# Initialize MCP server with proper name and description
mcp = FastMCP(
    "SheetCraft",
    description="A Google Sheets MCP server for data manipulation and analysis"
)

def decode_json(json_str: str) -> pd.DataFrame:
    """Convert JSON string to DataFrame, handling common encoding issues."""
    try:
        return pd.read_json(json_str, orient='split')
    except:
        if isinstance(json_str, str):
            json_str = json_str.replace('\\"', '"').replace('\\\\', '\\')
            if json_str.startswith('"') and json_str.endswith('"'):
                json_str = json_str[1:-1]
        return pd.read_json(json_str, orient='split')

# ----------------------------- Sheet Access Tools ----------------------------- 

## Tool 1: Fetch Google Sheet data
@mcp.tool(
    description="Fetch data from a Google Sheet and return as JSON",
    examples=[
        "Get data from the 'Budget' tab in my spreadsheet",
        "Fetch all records from 'Employees' sheet"
    ]
)
def fetch_google_sheet(sheet_url: str, tab_name: str) -> str:
    """Fetch data from a Google Sheet."""
    df = fetch_sheet(sheet_url, tab_name)
    return df.to_json(orient='split')

## Tool 2: Update Google Sheet
@mcp.tool(
    description="Update a Google Sheet with modified data",
    examples=[
        "Update the sheet with new data",
        "Save changes to the spreadsheet"
    ]
)
def update_google_sheet(sheet_url: str, tab_name: str, df_json: str) -> bool:
    """Update a Google Sheet with modified data."""
    df = decode_json(df_json)
    return update_sheet(sheet_url, tab_name, df)

# ----------------------------- Row Operation Tools ----------------------------- 

## Tool 3: Add new row
@mcp.tool(
    description="Add a new row to the Google Sheet",
    examples=[
        "Add a new employee with name 'John' and age '30'",
        "Insert a new record in the 'Transactions' sheet"
    ]
)
def add_row(sheet_url: str, tab_name: str, row_data: Dict[str, Any]) -> bool:
    """Add a new row to the Google Sheet."""
    df = fetch_sheet(sheet_url, tab_name)
    updated_df = add_data(df, row_data)
    return update_sheet(sheet_url, tab_name, updated_df)

## Tool 4: Edit row
@mcp.tool(
    description="Edit an existing row in the Google Sheet",
    examples=[
        "Update John's salary to 75000",
        "Change the status of order #123 to 'shipped'"
    ]
)
def edit_row(sheet_url: str, tab_name: str, row_identifier: Dict[str, Any], updated_data: Dict[str, Any]) -> bool:
    """Edit an existing row in the Google Sheet."""
    df = fetch_sheet(sheet_url, tab_name)
    updated_df = edit_data(df, row_identifier, updated_data)
    return update_sheet(sheet_url, tab_name, updated_df)

## Tool 5: Delete row
@mcp.tool(
    description="Delete a row from the Google Sheet",
    examples=[
        "Remove the employee with ID 'E123'",
        "Delete the transaction from yesterday"
    ]
)
def delete_row(sheet_url: str, tab_name: str, row_identifier: Dict[str, Any]) -> bool:
    """Delete a row from the Google Sheet."""
    df = fetch_sheet(sheet_url, tab_name)
    updated_df = delete_data(df, row_identifier)
    return update_sheet(sheet_url, tab_name, updated_df)

# ----------------------------- Column Operation Tools ----------------------------- 

## Tool 6: Add new column
@mcp.tool(
    description="Add a new calculated column to the Google Sheet",
    examples=[
        "Create a 'full_name' column by combining first and last names",
        "Add a 'total' column that sums up all expenses"
    ]
)
def add_sheet_column(sheet_url: str, tab_name: str, new_column_name: str, formula: str, 
                    reference_columns: List[str], params: Dict = None) -> bool:
    """Add a new calculated column to the Google Sheet.
    
    Args:
        sheet_url: URL of the Google Sheet
        tab_name: Name of the worksheet
        new_column_name: Name for the new column
        formula: Operation type ('concat', 'sum', 'multiply', 'divide', 'subtract')
        reference_columns: Columns to use in calculation
        params: Optional parameters for string operations
    """
    df = fetch_sheet(sheet_url, tab_name)
    updated_df = add_column(df, new_column_name, formula, reference_columns, params)
    return update_sheet(sheet_url, tab_name, updated_df)

## Tool 7: Rename column
@mcp.tool(
    description="Rename a column in the Google Sheet",
    examples=[
        "Rename 'phone_num' to 'contact_number'",
        "Change column 'addr' to 'address'"
    ]
)
def rename_sheet_column(sheet_url: str, tab_name: str, old_name: str, new_name: str) -> bool:
    """Rename a column in the Google Sheet."""
    df = fetch_sheet(sheet_url, tab_name)
    updated_df = rename_column(df, old_name, new_name)
    return update_sheet(sheet_url, tab_name, updated_df)

## Tool 8: Transform column
@mcp.tool(
    description="Transform values in a column using various operations",
    examples=[
        "Convert all prices to uppercase",
        "Format dates to MM/DD/YYYY"
    ]
)
def transform_sheet_column(sheet_url: str, tab_name: str, column_name: str, 
                         transformation: str, params: Dict = None) -> bool:
    """Transform values in a column using various operations."""
    df = fetch_sheet(sheet_url, tab_name)
    updated_df = transform_column(df, column_name, transformation, params)
    return update_sheet(sheet_url, tab_name, updated_df)

if __name__ == "__main__":
    # Set default port for MCP server
    port = int(os.environ.get("PORT", 8000))
    mcp.run(host="0.0.0.0", port=port)