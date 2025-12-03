"""Hotel recommendation tools."""

import json
import re
from langchain.tools import tool
from llm.config import llm

@tool
def get_hotel_recommendations(city: str, num_adults: int, num_kids: int, num_days: int) -> str:
    """Get hotel recommendations."""
    prompt = f"""Suggest 5 hotels in {city} for {num_adults} adults and {num_kids} kids for {num_days} nights.

For each hotel, provide:
- name, star_rating, price_per_night, currency, guest_rating, amenities (array), location, total_price

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