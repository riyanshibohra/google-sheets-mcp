# src/datacraft/server.py

from mcp.server.fastmcp import FastMCP
from tools.fetch_sheet import fetch_sheet, update_sheet
from tools.data_operations import add_data, edit_data, delete_data
from tools.column_operations import add_column, rename_column, transform_column
from typing import Dict, List, Any
import pandas as pd

mcp = FastMCP("SheetCraft")

def decode_json(json_str: str) -> pd.DataFrame:
    """Helper function to decode JSON string to DataFrame"""
    try:
        return pd.read_json(json_str, orient='split')
    except:
        # If direct parsing fails, try cleaning the string
        if isinstance(json_str, str):
            json_str = json_str.replace('\\"', '"').replace('\\\\', '\\')
            if json_str.startswith('"') and json_str.endswith('"'):
                json_str = json_str[1:-1]
        return pd.read_json(json_str, orient='split')

# ----------------------------- Sheet Access Tools ----------------------------- 

## Tool 1: Fetch Google Sheet data
@mcp.tool()
def fetch_google_sheet(sheet_url: str, tab_name: str) -> str:
    """
    Fetch data from a Google Sheet
    Args:
        sheet_url: URL of the Google Sheet
        tab_name: Name of the worksheet to fetch
    Returns:
        JSON string of the sheet data
    """
    df = fetch_sheet(sheet_url, tab_name)
    return df.to_json(orient='split')  # Only JSON conversion is for API response

## Tool 2: Update Google Sheet
@mcp.tool()
def update_google_sheet(sheet_url: str, tab_name: str, df_json: str) -> bool:
    """
    Update the Google Sheet with modified data
    Args:
        sheet_url: URL of the Google Sheet
        tab_name: Name of the worksheet to update
        df_json: Modified dataset in JSON format
    Returns:
        True if update was successful
    """
    df = decode_json(df_json)
    return update_sheet(sheet_url, tab_name, df)

# ----------------------------- Row Operation Tools ----------------------------- 

## Tool 3: Add new row
@mcp.tool()
def add_row(sheet_url: str, tab_name: str, row_data: Dict[str, Any]) -> bool:
    """
    Add a new row to the dataset
    Args:
        sheet_url: URL of the Google Sheet
        tab_name: Name of the worksheet
        row_data: Dictionary containing the new row data
    Returns:
        True if update was successful
    """
    df = fetch_sheet(sheet_url, tab_name)
    updated_df = add_data(df, row_data)
    return update_sheet(sheet_url, tab_name, updated_df)

## Tool 4: Edit row
@mcp.tool()
def edit_row(sheet_url: str, tab_name: str, row_identifier: Dict[str, Any], updated_data: Dict[str, Any]) -> bool:
    """
    Edit an existing row in the dataset
    Args:
        sheet_url: URL of the Google Sheet
        tab_name: Name of the worksheet
        row_identifier: Dictionary to identify the row (e.g., {"id": 123} or {"name": "John"})
        updated_data: Dictionary containing fields to update
    Returns:
        True if update was successful
    """
    df = fetch_sheet(sheet_url, tab_name)
    updated_df = edit_data(df, row_identifier, updated_data)
    return update_sheet(sheet_url, tab_name, updated_df)

## Tool 5: Delete row
@mcp.tool()
def delete_row(sheet_url: str, tab_name: str, row_identifier: Dict[str, Any]) -> bool:
    """
    Delete a row from the dataset
    Args:
        sheet_url: URL of the Google Sheet
        tab_name: Name of the worksheet
        row_identifier: Dictionary to identify the row to delete
    Returns:
        True if update was successful
    """
    df = fetch_sheet(sheet_url, tab_name)
    updated_df = delete_data(df, row_identifier)
    return update_sheet(sheet_url, tab_name, updated_df)

# ----------------------------- Column Operation Tools ----------------------------- 

## Tool 6: Add new column
@mcp.tool()
def add_sheet_column(sheet_url: str, tab_name: str, new_column_name: str, formula: str, reference_columns: List[str]) -> bool:
    """
    Add a new column based on calculations from other columns
    Args:
        sheet_url: URL of the Google Sheet
        tab_name: Name of the worksheet
        new_column_name: Name for the new column
        formula: Type of operation ('concat', 'sum', 'multiply', 'divide', 'subtract')
        reference_columns: List of columns to use in the calculation
    Returns:
        True if update was successful
    """
    df = fetch_sheet(sheet_url, tab_name)
    updated_df = add_column(df, new_column_name, formula, reference_columns)
    return update_sheet(sheet_url, tab_name, updated_df)

## Tool 7: Rename column
@mcp.tool()
def rename_sheet_column(sheet_url: str, tab_name: str, old_name: str, new_name: str) -> bool:
    """
    Rename a column in the dataset
    Args:
        sheet_url: URL of the Google Sheet
        tab_name: Name of the worksheet
        old_name: Current name of the column
        new_name: New name for the column
    Returns:
        True if update was successful
    """
    df = fetch_sheet(sheet_url, tab_name)
    updated_df = rename_column(df, old_name, new_name)
    return update_sheet(sheet_url, tab_name, updated_df)

## Tool 8: Transform column
@mcp.tool()
def transform_sheet_column(sheet_url: str, tab_name: str, column_name: str, transformation: str, params: Dict = None) -> bool:
    """
    Transform values in a column
    Args:
        sheet_url: URL of the Google Sheet
        tab_name: Name of the worksheet
        column_name: Name of the column to transform
        transformation: Type of transformation ('uppercase', 'lowercase', 'round', 'format_date')
        params: Additional parameters for the transformation
    Returns:
        True if update was successful
    """
    df = fetch_sheet(sheet_url, tab_name)
    updated_df = transform_column(df, column_name, transformation, params)
    return update_sheet(sheet_url, tab_name, updated_df)

if __name__ == "__main__":
    mcp.run()