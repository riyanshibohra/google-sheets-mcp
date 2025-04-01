# MCP Server - Google Sheets

A Model Context Protocol (MCP) server that provides powerful tools for interacting with Google Sheets. Built with pandas for efficient data manipulation and gspread for Google Sheets integration.

## Features

- Pandas-based data manipulation for efficient operations
- Complete CRUD operations for Google Sheets
- Advanced column operations (add, rename, transform)
- Row-level operations (add, edit, delete)
- JSON-based data exchange
- MCP integration for AI assistants

## Prerequisites

- Python 3.8 or higher
- Google Cloud Platform project with Sheets API enabled
- Google Sheets API credentials (`credentials.json`)
- MCP-compatible AI assistant (e.g., Claude)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/agent-project.git
cd agent-project
```

2. Set up your virtual environment using uv:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -e .
```

## Google Sheets Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Enable the Google Sheets API
4. Create credentials (OAuth 2.0 Client ID)
5. Download the credentials and save as `credentials.json` in your project root

## MCP Integration

### Setting up with Claude Desktop

Add this configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sheetcraft": {
      "command": "python",
      "args": ["src/server.py"],
      "env": {
        "CREDENTIALS_PATH": "/path/to/your/credentials.json"
      },
      "disabled": false
    }
  }
}
```

### Using with uv (Recommended)

```json
{
  "mcpServers": {
    "sheetcraft": {
      "command": "uv",
      "args": ["run", "python", "src/server.py"],
      "env": {
        "CREDENTIALS_PATH": "/path/to/your/credentials.json"
      },
      "disabled": false
    }
  }
}
```

### Example Prompts for Claude

You can use natural language to interact with your Google Sheets:

1. Basic Operations:
   ```
   "Get the data from the 'Budget' tab in my spreadsheet"
   "Add a new row with name 'John' and age '30' to the 'Employees' sheet"
   "Update the salary for employee 'John Smith' to 75000"
   ```

2. Column Operations:
   ```
   "Create a new column 'full_name' by combining 'first_name' and 'last_name'"
   "Calculate the total expenses by adding the 'rent' and 'utilities' columns"
   "Rename the 'phone_num' column to 'contact_number'"
   ```

3. Data Transformations:
   ```
   "Convert all values in the 'price' column to uppercase"
   "Format the 'date' column to MM/DD/YYYY"
   "Calculate the percentage of total for each value in 'sales' column"
   ```

## Available Tools

### Sheet Access Tools
1. `fetch_google_sheet(sheet_url: str, tab_name: str) -> str`
   - Fetches data from a Google Sheet
   - Returns JSON string of sheet data

2. `update_google_sheet(sheet_url: str, tab_name: str, df_json: str) -> bool`
   - Updates sheet with provided data
   - Data should be in JSON format

### Row Operations
3. `add_row(sheet_url: str, tab_name: str, row_data: Dict[str, Any]) -> bool`
   - Adds a new row to the sheet
   - row_data: Dictionary of column:value pairs

4. `edit_row(sheet_url: str, tab_name: str, row_identifier: Dict[str, Any], updated_data: Dict[str, Any]) -> bool`
   - Edits an existing row
   - row_identifier: Dictionary to identify the row
   - updated_data: New values for the row

5. `delete_row(sheet_url: str, tab_name: str, row_identifier: Dict[str, Any]) -> bool`
   - Deletes a row from the sheet
   - row_identifier: Dictionary to identify the row

### Column Operations
6. `add_sheet_column(sheet_url: str, tab_name: str, new_column_name: str, formula: str, reference_columns: List[str], params: Dict = None) -> bool`
   - Adds a calculated column
   - Supported formulas: 'concat', 'sum', 'multiply', 'divide', 'subtract'

7. `rename_sheet_column(sheet_url: str, tab_name: str, old_name: str, new_name: str) -> bool`
   - Renames an existing column

8. `transform_sheet_column(sheet_url: str, tab_name: str, column_name: str, transformation: str, params: Dict = None) -> bool`
   - Applies transformations to column values

## Usage Examples

```python
# Fetch data from a sheet
result = fetch_google_sheet(
    "https://docs.google.com/spreadsheets/d/your-sheet-id",
    "Sheet1"
)

# Add a new row
add_row(
    "https://docs.google.com/spreadsheets/d/your-sheet-id",
    "Sheet1",
    {"name": "John", "age": 30, "city": "New York"}
)

# Add a calculated column
add_sheet_column(
    "https://docs.google.com/spreadsheets/d/your-sheet-id",
    "Sheet1",
    "full_name",
    "concat",
    ["first_name", "last_name"],
    {"separator": " "}
)
```

## Running in Development

```bash
# Start the MCP server
python src/server.py
```

## Docker Support

Build and run with Docker:

```bash
# Build the image
docker build -t sheetcraft .

# Run the container
docker run -p 8000:8000 -v $(pwd)/credentials.json:/app/credentials.json sheetcraft
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

MIT License