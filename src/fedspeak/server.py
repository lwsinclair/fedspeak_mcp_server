"""
FedSpeak MCP Server
===============

This module implements an MCP server for the Federal Reserve statements and data.
It provides tools for searching and analyzing Federal Reserve statements.
"""

import asyncio
import logging
import sys
import aiohttp
import mcp.types as types
from mcp.server import Server, InitializationOptions, NotificationOptions
from mcp.server.stdio import stdio_server
from typing import Dict, Any, List, Optional

from .config import Settings
from .tools.search import search_tool, get_metadata_tool, analyze_trends_tool, get_latest_statement_tool
from .prompts import PROMPTS, PROMPT_HANDLERS

# Initialize server settings
settings = Settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(settings.LOG_FILE, mode="a")
    ]
)
logger = logging.getLogger("fedspeak-mcp-server")

# Initialize MCP server
server = Server(settings.APP_NAME)

@server.list_tools()
async def list_tools() -> List[types.Tool]:
    """List available tools for Federal Reserve statement analysis."""
    return [
        search_tool,
        get_metadata_tool,
        analyze_trends_tool,
        get_latest_statement_tool
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls by proxying to private API."""
    logger.info(f"Tool call: {name} with arguments: {arguments}")
    
    try:
        # Forward request to private API server
        async with aiohttp.ClientSession() as session:
            # Determine HTTP method based on tool name
            if name == "get_latest_statement":
                # GET request for get_latest_statement endpoint
                async with session.get(
                    f"{settings.API_ENDPOINT}/api/tools/{name}",
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"API error: {error_text}")
                        return [types.TextContent(
                            type="text", 
                            text=f"Error: The FOMC data service returned an error: {error_text}"
                        )]
                    
                    result = await response.json()
                    return [types.TextContent(
                        type="text",
                        text=result.get("content", "No content returned from API")
                    )]
            else:
                # POST request for all other endpoints
                async with session.post(
                    f"{settings.API_ENDPOINT}/api/tools/{name}",
                    json=arguments,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"API error: {error_text}")
                        return [types.TextContent(
                            type="text", 
                            text=f"Error: The FOMC data service returned an error: {error_text}"
                        )]
                    
                    result = await response.json()
                    return [types.TextContent(
                        type="text",
                        text=result.get("content", "No content returned from API")
                    )]
    except Exception as e:
        logger.error(f"Error calling private API: {str(e)}", exc_info=True)
        return [types.TextContent(
            type="text",
            text=f"Error: Could not connect to FOMC data service: {str(e)}"
        )]

@server.list_prompts()
async def list_prompts() -> List[types.Prompt]:
    """List available prompts for Federal Reserve analysis."""
    return list(PROMPTS.values())

@server.get_prompt()
async def get_prompt(name: str, arguments: Dict[str, str] | None = None) -> types.GetPromptResult:
    """Handle prompt requests for Federal Reserve analysis templates."""
    try:
        if name in PROMPT_HANDLERS:
            handler = PROMPT_HANDLERS[name]
            return await handler(arguments if arguments else {})
        else:
            raise ValueError(f"Unknown prompt: {name}")
    except Exception as e:
        logger.error(f"Error handling prompt {name}: {str(e)}")
        raise ValueError(f"Error handling prompt: {str(e)}")

async def main():
    """Run the server as an async context."""
    logger.info(f"Starting {settings.APP_NAME} MCP Server v{settings.APP_VERSION}")
    
    # Ensure storage directory exists
    settings.STORAGE_PATH.mkdir(parents=True, exist_ok=True)
    
    # Test API connection
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{settings.API_ENDPOINT}/health") as response:
                if response.status != 200:
                    logger.warning(f"API server health check failed: {await response.text()}")
                else:
                    logger.info("API server connection successful")
    except Exception as e:
        logger.warning(f"Could not connect to API server: {str(e)}")
    
    # Start the MCP server
    async with stdio_server() as streams:
        await server.run(
            streams[0],
            streams[1],
            InitializationOptions(
                server_name=settings.APP_NAME,
                server_version=settings.APP_VERSION,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

# If script is run directly
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)
