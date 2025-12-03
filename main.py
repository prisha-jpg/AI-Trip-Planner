"""
AI Travel Planner - Main Application Entry Point

A modular, comprehensive API for AI-powered travel planning with LangGraph.
This file orchestrates all the components and starts the server.
"""

import uvicorn
from api.app import create_app
from config.settings import settings

def main():
    """Main function to start the application."""
    # Create the FastAPI app
    app = create_app()
    
    # Start the server
    uvicorn.run(
        app, 
        host=settings.HOST, 
        port=settings.PORT
    )

if __name__ == "__main__":
    main()