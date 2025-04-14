"""Configuration settings for the FOMC MCP server."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os


class Settings(BaseSettings):   
    """Server configuration settings."""

    APP_NAME: str = "fedspeak"
    APP_VERSION: str = "1.0.0"
    API_ENDPOINT: str = os.environ.get("FEDSPEAK_API_ENDPOINT", "https://fedspeak-mcp-backend-671377599496.us-central1.run.app")
    
    # Path settings
    STORAGE_PATH: Path = Path.home() / ".fedspeak-mcp-server" / "data"
    
    # Logging settings
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.environ.get("LOG_FILE", "fedspeak_mcp_server.log")
    
    # Allow extra fields from environment variables
    model_config = SettingsConfigDict(extra="allow")
