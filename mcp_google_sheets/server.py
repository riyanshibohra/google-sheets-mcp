# src/server.py

from mcp.server.fastmcp import FastMCP
from tools.fetch_sheet import fetch_sheet, update_sheet
from tools.data_operations import add_data, edit_data, delete_data
from tools.column_operations import add_column, rename_column, transform_column
from typing import Dict, List, Any, Optional, AsyncGenerator
from dataclasses import dataclass
from contextlib import asynccontextmanager
import pandas as pd
import asyncio
import logging
import os
from functools import wraps
import typer

# Configure logging
logger = logging.getLogger(__name__)

# Data Models
@dataclass
class SheetConfig:
    """Configuration for Google Sheet operations."""
    sheet_url: str
    tab_name: str

@dataclass
class ColumnOperation:
    """Configuration for column operations."""
    name: str
    formula: Optional[str] = None
    reference_columns: Optional[List[str]] = None
    params: Optional[Dict[str, Any]] = None

@dataclass
class ServerConfig:
    """Server configuration settings."""
    host: str = "0.0.0.0"
    port: int = 8000
    name: str = "Google Sheets MCP"
    description: str = "A Google Sheets MCP server for data manipulation and analysis"

# Server Lifecycle Management
@asynccontextmanager
async def lifespan(config: ServerConfig) -> AsyncGenerator[None, None]:
    """Server lifespan context manager."""
    logger.info(f"Starting {config.name} server...")
    try:
        yield
    finally:
        logger.info(f"Shutting down {config.name} server...")
        await asyncio.sleep(0.1)

class GoogleSheetsMCPServer:
    """Main server class for Google Sheets MCP operations."""
    
    def __init__(self, config: ServerConfig):
        """Initialize the server with configuration."""
        self.config = config
        self.mcp = FastMCP(config.name, description=config.description)
        self._setup_logging()
        self.register_tools()

    def _setup_logging(self):
        """Configure logging for the server."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    @staticmethod
    async def _run_in_thread(func, *args, **kwargs):
        """Helper method to run synchronous functions in a thread pool."""
        return await asyncio.to_thread(func, *args, **kwargs)

    @staticmethod
    async def decode_json(json_str: str) -> pd.DataFrame:
        """Convert JSON string to DataFrame, handling common encoding issues."""
        try:
            return pd.read_json(json_str, orient='split')
        except Exception as e:
            logger.error(f"Error decoding JSON: {e}")
            if isinstance(json_str, str):
                json_str = json_str.replace('\\"', '"').replace('\\\\', '\\')
                if json_str.startswith('"') and json_str.endswith('"'):
                    json_str = json_str[1:-1]
            return pd.read_json(json_str, orient='split')

    def register_tools(self):
        """Register all tools with the MCP server."""
        # Sheet Access Tools
        self.mcp.tool(
            description="Fetch data from a Google Sheet and return as JSON"
        )(self.fetch_google_sheet)

        self.mcp.tool(
            description="Update a Google Sheet with modified data"
        )(self.update_google_sheet)

        # Row Operation Tools
        self.mcp.tool(
            description="Add a new row to the Google Sheet"
        )(self.add_row)

        self.mcp.tool(
            description="Edit an existing row in the Google Sheet"
        )(self.edit_row)

        self.mcp.tool(
            description="Delete a row from the Google Sheet"
        )(self.delete_row)

        # Column Operation Tools
        self.mcp.tool(
            description="Add a new calculated column to the Google Sheet"
        )(self.add_sheet_column)

        self.mcp.tool(
            description="Rename a column in the Google Sheet"
        )(self.rename_sheet_column)

        self.mcp.tool(
            description="Transform values in a column using various operations"
        )(self.transform_sheet_column)

    async def fetch_google_sheet(self, sheet_url: str, tab_name: str) -> str:
        """Fetch data from a Google Sheet."""
        sheet_config = SheetConfig(sheet_url=sheet_url, tab_name=tab_name)
        logger.info(f"Fetching sheet: {sheet_config.tab_name}")
        try:
            df = await self._run_in_thread(fetch_sheet, sheet_config.sheet_url, sheet_config.tab_name)
            return df.to_json(orient='split')
        except Exception as e:
            logger.error(f"Error fetching sheet: {e}")
            raise

    async def update_google_sheet(self, sheet_url: str, tab_name: str, df_json: str) -> bool:
        """Update a Google Sheet with modified data."""
        sheet_config = SheetConfig(sheet_url=sheet_url, tab_name=tab_name)
        logger.info(f"Updating sheet: {sheet_config.tab_name}")
        try:
            df = await self.decode_json(df_json)
            return await self._run_in_thread(update_sheet, sheet_config.sheet_url, sheet_config.tab_name, df)
        except Exception as e:
            logger.error(f"Error updating sheet: {e}")
            raise

    async def add_row(self, sheet_url: str, tab_name: str, row_data: Dict[str, Any]) -> bool:
        """Add a new row to the Google Sheet."""
        sheet_config = SheetConfig(sheet_url=sheet_url, tab_name=tab_name)
        logger.info(f"Adding row to sheet: {sheet_config.tab_name}")
        try:
            df = await self._run_in_thread(fetch_sheet, sheet_config.sheet_url, sheet_config.tab_name)
            updated_df = await self._run_in_thread(add_data, df, row_data)
            return await self._run_in_thread(update_sheet, sheet_config.sheet_url, sheet_config.tab_name, updated_df)
        except Exception as e:
            logger.error(f"Error adding row: {e}")
            raise

    async def edit_row(self, sheet_url: str, tab_name: str, row_identifier: Dict[str, Any], updated_data: Dict[str, Any]) -> bool:
        """Edit an existing row in the Google Sheet."""
        sheet_config = SheetConfig(sheet_url=sheet_url, tab_name=tab_name)
        logger.info(f"Editing row in sheet: {sheet_config.tab_name}")
        try:
            df = await self._run_in_thread(fetch_sheet, sheet_config.sheet_url, sheet_config.tab_name)
            updated_df = await self._run_in_thread(edit_data, df, row_identifier, updated_data)
            return await self._run_in_thread(update_sheet, sheet_config.sheet_url, sheet_config.tab_name, updated_df)
        except Exception as e:
            logger.error(f"Error editing row: {e}")
            raise

    async def delete_row(self, sheet_url: str, tab_name: str, row_identifier: Dict[str, Any]) -> bool:
        """Delete a row from the Google Sheet."""
        sheet_config = SheetConfig(sheet_url=sheet_url, tab_name=tab_name)
        logger.info(f"Deleting row from sheet: {sheet_config.tab_name}")
        try:
            df = await self._run_in_thread(fetch_sheet, sheet_config.sheet_url, sheet_config.tab_name)
            updated_df = await self._run_in_thread(delete_data, df, row_identifier)
            return await self._run_in_thread(update_sheet, sheet_config.sheet_url, sheet_config.tab_name, updated_df)
        except Exception as e:
            logger.error(f"Error deleting row: {e}")
            raise

    async def add_sheet_column(
        self, 
        sheet_url: str, 
        tab_name: str, 
        new_column_name: str, 
        formula: str,
        reference_columns: List[str], 
        params: Optional[Dict] = None
    ) -> bool:
        """Add a new calculated column to the Google Sheet."""
        sheet_config = SheetConfig(sheet_url=sheet_url, tab_name=tab_name)
        column_op = ColumnOperation(
            name=new_column_name,
            formula=formula,
            reference_columns=reference_columns,
            params=params
        )
        logger.info(f"Adding column {column_op.name} to sheet: {sheet_config.tab_name}")
        try:
            df = await self._run_in_thread(fetch_sheet, sheet_config.sheet_url, sheet_config.tab_name)
            updated_df = await self._run_in_thread(
                add_column, 
                df, 
                column_op.name, 
                column_op.formula, 
                column_op.reference_columns, 
                column_op.params
            )
            return await self._run_in_thread(update_sheet, sheet_config.sheet_url, sheet_config.tab_name, updated_df)
        except Exception as e:
            logger.error(f"Error adding column: {e}")
            raise

    async def rename_sheet_column(self, sheet_url: str, tab_name: str, old_name: str, new_name: str) -> bool:
        """Rename a column in the Google Sheet."""
        sheet_config = SheetConfig(sheet_url=sheet_url, tab_name=tab_name)
        logger.info(f"Renaming column from {old_name} to {new_name} in sheet: {sheet_config.tab_name}")
        try:
            df = await self._run_in_thread(fetch_sheet, sheet_config.sheet_url, sheet_config.tab_name)
            updated_df = await self._run_in_thread(rename_column, df, old_name, new_name)
            return await self._run_in_thread(update_sheet, sheet_config.sheet_url, sheet_config.tab_name, updated_df)
        except Exception as e:
            logger.error(f"Error renaming column: {e}")
            raise

    async def transform_sheet_column(
        self, 
        sheet_url: str, 
        tab_name: str, 
        column_name: str,
        transformation: str, 
        params: Optional[Dict] = None
    ) -> bool:
        """Transform values in a column using various operations."""
        sheet_config = SheetConfig(sheet_url=sheet_url, tab_name=tab_name)
        column_op = ColumnOperation(name=column_name, params=params)
        logger.info(f"Transforming column {column_op.name} in sheet: {sheet_config.tab_name}")
        try:
            df = await self._run_in_thread(fetch_sheet, sheet_config.sheet_url, sheet_config.tab_name)
            updated_df = await self._run_in_thread(
                transform_column, 
                df, 
                column_op.name, 
                transformation, 
                column_op.params
            )
            return await self._run_in_thread(update_sheet, sheet_config.sheet_url, sheet_config.tab_name, updated_df)
        except Exception as e:
            logger.error(f"Error transforming column: {e}")
            raise

    def start(self):
        """Start the server."""
        # Set port through environment variable before running
        os.environ["PORT"] = str(self.config.port)
        logger.info(f"Starting {self.config.name} server on port {self.config.port}...")
        self.mcp.run()

app = typer.Typer()

@app.command()
def start(
    port: int = typer.Option(8000, help="Port to run the server on"),
    name: str = typer.Option("Google Sheets MCP", help="Name of the server"),
    description: str = typer.Option(
        "A Google Sheets MCP server for data manipulation and analysis",
        help="Description of the server"
    )
):
    """Start the Google Sheets MCP server."""
    config = ServerConfig(
        port=port,
        name=name,
        description=description
    )
    server = GoogleSheetsMCPServer(config)
    server.start()

def main():
    """Entry point for the CLI."""
    app()

if __name__ == "__main__":
    main()