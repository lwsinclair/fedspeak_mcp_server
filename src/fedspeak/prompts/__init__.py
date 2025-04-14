"""
Prompt templates for the FOMC MCP server.

This module contains reusable prompt templates to guide users in using the 
available FOMC analysis tools effectively.
"""

import mcp.types as types
from typing import Dict, Any

# Define available prompts
PROMPTS = {
    "search-guidance": types.Prompt(
        name="search-guidance",
        description="How to effectively search FOMC statements",
        arguments=[
            types.PromptArgument(
                name="topic",
                description="Topic you want to search for (e.g., inflation, interest rates)",
                required=False
            )
        ],
    ),
    "analyze-trends-guidance": types.Prompt(
        name="analyze-trends-guidance",
        description="How to analyze trends in FOMC language over time",
        arguments=[
            types.PromptArgument(
                name="topic",
                description="Topic to analyze (e.g., inflation, economic growth)",
                required=False
            )
        ],
    ),
    "latest-statement-analysis": types.Prompt(
        name="latest-statement-analysis",
        description="How to analyze the latest FOMC statement",
        arguments=[],
    )
}

async def handle_search_guidance(arguments: Dict[str, str]) -> types.GetPromptResult:
    """Guide users on how to effectively search FOMC statements."""
    topic = arguments.get("topic", "monetary policy")
    
    return types.GetPromptResult(
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"I want to find information about {topic} in Federal Reserve statements. What's the best approach?"
                )
            ),
            types.PromptMessage(
                role="assistant",
                content=types.TextContent(
                    type="text",
                    text=f"To search for information about {topic} in Federal Reserve statements, I recommend using the `search_fomc_statements` tool with the following parameters:\n\n"
                         f"- Set `query` to a specific question about {topic} (e.g., \"How has the Fed's stance on {topic} changed in recent years?\")\n"
                         f"- Optional: Use `start_date` and `end_date` to narrow the time period (format: YYYY-MM-DD)\n"
                         f"- Optional: Set `top_k` to control the number of results (default: 5)\n"
                         f"- Optional: Set `include_full_text` to true if you need the complete statements\n\n"
                         f"For example:\n"
                         f"```\n"
                         f"search_fomc_statements(query=\"Fed's stance on {topic}\", top_k=3, start_date=\"2020-01-01\", include_full_text=false)\n"
                         f"```\n\n"
                         f"After getting search results, you can use the `get_fomc_metadata` tool to get additional context about specific statements."
                )
            )
        ]
    )

async def handle_analyze_trends_guidance(arguments: Dict[str, str]) -> types.GetPromptResult:
    """Guide users on how to analyze trends in FOMC language."""
    topic = arguments.get("topic", "inflation")
    
    return types.GetPromptResult(
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"How can I analyze trends in how the Fed discusses {topic} over time?"
                )
            ),
            types.PromptMessage(
                role="assistant",
                content=types.TextContent(
                    type="text",
                    text=f"To analyze trends in how the Federal Reserve discusses {topic} over time, the `analyze_fomc_trends` tool is most appropriate. Here's how to use it effectively:\n\n"
                         f"1. Call the tool with the following parameters:\n"
                         f"   - `topic`: \"{topic}\" (required)\n"
                         f"   - `start_date`: Beginning of your analysis period (e.g., \"2018-01-01\")\n" 
                         f"   - `end_date`: End of your analysis period (e.g., \"2023-12-31\")\n"
                         f"   - `chair`: Optionally filter by Fed Chair name (e.g., \"Powell\")\n\n"
                         f"Example:\n"
                         f"```\n"
                         f"analyze_fomc_trends(topic=\"{topic}\", start_date=\"2018-01-01\", end_date=\"2023-12-31\")\n"
                         f"```\n\n"
                         f"The results will show how the language, frequency, and context around {topic} have evolved over the specified time period. "
                         f"You can follow up with the `search_fomc_statements` tool to dive deeper into specific statements identified in the trend analysis."
                )
            )
        ]
    )

async def handle_latest_statement_analysis(arguments: Dict[str, str]) -> types.GetPromptResult:
    """Guide users on analyzing the latest FOMC statement."""
    
    return types.GetPromptResult(
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text="How can I analyze the most recent Federal Reserve statement?"
                )
            ),
            types.PromptMessage(
                role="assistant",
                content=types.TextContent(
                    type="text",
                    text="To analyze the most recent Federal Reserve statement, follow these steps:\n\n"
                         "1. First, retrieve the latest statement using the `get_latest_statement` tool:\n"
                         "   ```\n"
                         "   get_latest_statement()\n"
                         "   ```\n\n"
                         "2. Once you have the statement text, you can ask specific questions about it, such as:\n"
                         "   - What is the Fed's current policy stance?\n"
                         "   - Did they change interest rates?\n"
                         "   - What is their outlook on inflation and employment?\n"
                         "   - How does this statement differ from previous ones?\n\n"
                         "3. For historical context, you can use the `search_fomc_statements` tool to find related past statements:\n"
                         "   ```\n"
                         "   search_fomc_statements(query=\"Similar language to the latest statement regarding inflation\", top_k=3)\n"
                         "   ```\n\n"
                         "4. To understand broader trends, you might want to use the `analyze_fomc_trends` tool with recent date ranges."
                )
            )
        ]
    )

# Mapping of prompt names to their handler functions
PROMPT_HANDLERS = {
    "search-guidance": handle_search_guidance,
    "analyze-trends-guidance": handle_analyze_trends_guidance,
    "latest-statement-analysis": handle_latest_statement_analysis
}
