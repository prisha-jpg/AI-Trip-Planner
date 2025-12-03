"""Attractions and places tools."""

import json
import re
from langchain.tools import tool
from llm.config import llm

@tool
def get_top_attractions(city: str, num_days: int = 3) -> str:
    """Get top attractions for a city."""
    prompt = f"""List the top {min(num_days * 3, 10)} attractions in {city}.

For each attraction, provide:
- name: Attraction name
- description: Brief description (1 sentence)
- category: Type (Museum, Park, Monument, etc.)
- ticket_price: Estimated ticket price in local currency (number only, if free put 0)
- currency: Currency code (USD, EUR, INR, etc.)
- duration: Recommended visit time (e.g., "2 hours", "Half day")
- rating: Tourist rating out of 5

Return ONLY a valid JSON array."""
    
    try:
        response = llm.invoke(prompt)
        content = response.content
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        
        if json_match:
            return json_match.group()
        return json.dumps([{"error": "No data"}])
    except Exception as e:
        return json.dumps([{"error": str(e)}])

@tool
def get_nearby_places(city: str) -> str:
    """Get nearby places worth visiting."""
    prompt = f"""List 6 cities near {city}. For each: name, distance_km, transport, famous_for, recommended_duration, estimated_cost. Return JSON array."""
    
    try:
        response = llm.invoke(prompt)
        json_match = re.search(r'\[.*\]', response.content, re.DOTALL)
        return json_match.group() if json_match else json.dumps([{"error": "No data"}])
    except Exception as e:
        return json.dumps([{"error": str(e)}])