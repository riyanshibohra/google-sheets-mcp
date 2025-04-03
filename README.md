# Google Sheets MCP Server

A Model Context Protocol server for manipulating and analyzing Google Sheets data.

## Features

- Fetch and update sheet data
- Add, edit, and delete rows
- Add, rename, and transform columns
- Proper async implementation for better performance
- ntegration with Claude Desktop


## Installation

### Using uvx (recommended)

```bash
uvx google-sheets-mcp
```

### For Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd google-sheets-mcp
```

2. Create a virtual environment with uv:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
```

3. Install dependencies:
```bash
uv pip install -r requirements.txt
```

## Usage with Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "uvx",
      "args": ["google-sheets-mcp"],
      "env": {
        "SERVICE_ACCOUNT_PATH": "/path/to/your/service-account-key.json",
        "DRIVE_FOLDER_ID": "your_shared_folder_id_here"
      }
    }
  }
}
```

### Alternative Authentication Method

For OAuth authentication, use this configuration instead:

```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "uvx",
      "args": ["google-sheets-mcp"],
      "env": {
        "CREDENTIALS_PATH": "/path/to/your/credentials.json",
        "TOKEN_PATH": "/path/to/your/token.json"
      }
    }
  }
}
```

## Example Prompts for Claude

Once connected, you can use prompts like:

- "Fetch data from Sheet1 in my spreadsheet"
- "Add a new row with name 'John' and age '30'"
- "Update the 'status' column for row with ID '123' to 'completed'"
- "Add a new calculated column 'full_name' by combining first and last name"
- "Delete the row where email is 'john@example.com'"
- "Transform the 'date' column to MM/DD/YYYY format"

## Development

To run the server locally:

```bash
# First check if port 8000 is available
lsof -i :8000

# Start the server
python src/server.py

# Verify the server is running
curl http://localhost:8000/health
```

The server will start on port 8000 by default. You can change this by setting the `PORT` environment variable.

## License

MIT License - See LICENSE file for details
