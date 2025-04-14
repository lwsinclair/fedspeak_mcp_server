"""
FEDSPEAK Search Tools

This module defines tools for searching, retrieving, and analyzing Federal Reserve statements.
"""

import mcp.types as types
import logging
from typing import Dict, Any, List

logger = logging.getLogger("fedspeak-mcp-server.tools")

# Define the search tool for semantic search of FOMC statements
search_tool = types.Tool(
    name="search_fomc_statements",
    description="Search Federal Reserve (FOMC) statements semantically",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Natural language query about Fed policy, decisions, or statements"
            },
            "top_k": {
                "type": "integer",
                "description": "Number of results to return (default: 5)"
            },
            "start_date": {
                "type": "string",
                "description": "Filter by start date (YYYY-MM-DD)"
            },
            "end_date": {
                "type": "string",
                "description": "Filter by end date (YYYY-MM-DD)"
            },
            "include_full_text": {
                "type": "boolean",
                "description": "Whether to include the full statement text (default: false)"
            }
        },
        "required": ["query"]
    }
)

# Define the metadata tool for retrieving statement metadata
get_metadata_tool = types.Tool(
    name="get_fomc_metadata",
    description="Get metadata about available FOMC statements",
    inputSchema={
        "type": "object",
        "properties": {
            "start_date": {
                "type": "string",
                "description": "Start date (YYYY-MM-DD)"
            },
            "end_date": {
                "type": "string",
                "description": "End date (YYYY-MM-DD)"
            },
            "chair": {
                "type": "string",
                "description": "Filter by Fed Chair name"
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of results to return (default: 10)"
            }
        }
    }
)

# Define the trends analysis tool
analyze_trends_tool = types.Tool(
    name="analyze_fomc_trends",
    description="Analyze trends in Federal Reserve language over time",
    inputSchema={
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "Topic to analyze (e.g., 'inflation', 'interest rates', 'economic growth')"
            },
            "start_date": {
                "type": "string",
                "description": "Start date (YYYY-MM-DD)"
            },
            "end_date": {
                "type": "string",
                "description": "End date (YYYY-MM-DD)"
            },
            "chair": {
                "type": "string",
                "description": "Filter by Fed Chair name"
            }
        },
        "required": ["topic"]
    }
)

# Define the latest statement tool
get_latest_statement_tool = types.Tool(
    name="get_latest_statement",
    description="Get the most recent FOMC statement with full text",
    inputSchema={
        "type": "object",
        "properties": {},
        "required": []
    }
)

# Note: The actual implementation of these tool handlers is in the main server.py
# as it proxies requests to the private API. This file just defines the tool schemas.
