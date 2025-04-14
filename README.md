# Fedspeak MCP Server

A Model Context Protocol (MCP) server for accessing and analyzing Federal Reserve (FOMC) statements.

## Overview

This server provides a secure way to interact with a Federal Reserve statements database using the Model Context Protocol. It follows the Proxy Server Architecture pattern, where this public component contains no sensitive credentials and forwards requests to a private API server that contains the actual database access logic.

## Features

- **Search Statements**: Semantically search FOMC statements by topic, date, or content
- **Metadata Access**: Get information about available statements
- **Trend Analysis**: Analyze language trends in Fed statements over time
- **Resource Access**: Access full statement content as resources
- **Prompt Templates**: Use pre-defined prompt templates for common analysis tasks

## Installation

### Prerequisites

- Python 3.10 or higher
- A running private API server with access to the FOMC database

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/fomc-mcp-server.git
cd fomc-mcp-server

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
# Install with pip
pip install .

# Install with UV (recommended for exact dependency versions)
uv pip install .
```

## Configuration

The server can be configured using environment variables:

- `FEDSPEAK_API_ENDPOINT`: URL of the backend service that handles all database connections (Firestore) and retrieves FOMC statement data for search, analysis, and metadata operations (default: "https://fedspeak-mcp-backend-671377599496.us-central1.run.app")
- `LOG_LEVEL`: Logging level (default: "INFO")
- `LOG_FILE`: Log file path (default: "fedspeak_mcp_server.log")

**Note:** All database interactions (including Firestore) are handled by the backend API service. You do not need to configure any database credentials in this MCP server.

## Usage

### Running the Server

```bash
# Run directly
python -m fedspeak

# Or using the installed script
fedspeak
```

### Using with Claude for Desktop

To use with Claude for Desktop, add this server to your Claude configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fedspeak": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/mk/Documents/Python/AI Playground/mcp/fedspeak/src/fedspeak",
        "run",
        "fedspeak"
      ],
      "env": {
        "FEDSPEAK_API_ENDPOINT": "https://fedspeak-mcp-backend-671377599496.us-central1.run.app"
      }
    }
  }
}
```

> **Note:** This configuration uses UV to run the fedspeak server in a src-based package structure. The API endpoint connects to the Cloud Run backend service that handles all database operations and FOMC statement retrieval.

## Available Tools

- `search_fomc_statements`: Search Federal Reserve statements semantically
- `get_fomc_metadata`: Get metadata about available FOMC statements
- `analyze_fomc_trends`: Analyze trends in Federal Reserve language over time
- `get_latest_statement`: Get the most recent FOMC statement with full text

## Available Prompts

- `search-guidance`: How to effectively search FOMC statements
- `analyze-trends-guidance`: How to analyze trends in FOMC language over time
- `latest-statement-analysis`: How to analyze the latest FOMC statement

## License

MIT