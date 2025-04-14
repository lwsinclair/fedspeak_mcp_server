"""
Tool definitions for the FOMC MCP server.

This module contains the tool definitions and handlers for the server.
"""

from .search import search_tool, get_metadata_tool, analyze_trends_tool

# Export tools for use in the main server
__all__ = [
    "search_tool",
    "get_metadata_tool", 
    "analyze_trends_tool"
]
