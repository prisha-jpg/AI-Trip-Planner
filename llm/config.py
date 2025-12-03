"""LLM configuration and initialization."""

from langchain_groq import ChatGroq
from config.settings import settings

def get_llm():
    """Initialize and return the LLM instance."""
    return ChatGroq(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE
    )

def get_llm_with_tools(tools):
    """Get LLM instance with tools bound."""
    llm = get_llm()
    return llm.bind_tools(tools)

# Global LLM instance
llm = get_llm()