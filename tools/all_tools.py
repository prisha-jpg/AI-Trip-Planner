"""All tools for the travel planner."""

from .weather import get_weather_info
from .attractions import get_top_attractions, get_nearby_places
from .hotels import get_hotel_recommendations
from .currency import convert_currency

# Export all tools
all_tools = [
    get_weather_info,
    get_top_attractions,
    get_hotel_recommendations,
    convert_currency,
    get_nearby_places
]

__all__ = [
    'get_weather_info',
    'get_top_attractions',
    'get_hotel_recommendations',
    'convert_currency',
    'get_nearby_places',
    'all_tools'
]