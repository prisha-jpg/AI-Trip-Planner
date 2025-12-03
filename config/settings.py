"""Configuration settings for the AI Travel Planner."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings and environment variables."""
    
    # API Keys
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")
    
    # LLM Configuration
    LLM_MODEL = "openai/gpt-oss-120b"
    LLM_TEMPERATURE = 0.7
    
    # API Configuration
    API_TITLE = "AI Travel Planner API"
    API_DESCRIPTION = "A comprehensive API for AI-powered travel planning with LangGraph"
    API_VERSION = "1.0.0"
    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 8000
    
    def __init__(self):
        """Initialize settings and set environment variables."""
        if self.TAVILY_API_KEY:
            os.environ["TAVILY_API_KEY"] = self.TAVILY_API_KEY
        if self.GROQ_API_KEY:
            os.environ["GROQ_API_KEY"] = self.GROQ_API_KEY
        if self.OPENWEATHER_API_KEY:
            os.environ["OPENWEATHER_API_KEY"] = self.OPENWEATHER_API_KEY
        if self.EXCHANGERATE_API_KEY:
            os.environ["EXCHANGERATE_API_KEY"] = self.EXCHANGERATE_API_KEY

# Global settings instance
settings = Settings()