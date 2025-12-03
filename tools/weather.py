"""Weather-related tools."""

import json
import os
import requests
from datetime import datetime
from langchain.tools import tool

@tool
def get_weather_info(city: str, date: str = None) -> str:
    """Get weather information for a city."""
    try:
        api_key = os.environ.get("OPENWEATHER_API_KEY")
        if not api_key:
            return json.dumps({"error": "API key not configured"})
        
        # Get coordinates
        geo_url = "http://api.openweathermap.org/geo/1.0/direct"
        geo_params = {"q": city, "limit": 1, "appid": api_key}
        geo_response = requests.get(geo_url, params=geo_params, timeout=10)
        
        if geo_response.status_code != 200 or not geo_response.json():
            return json.dumps({"error": "City not found"})
        
        geo_data = geo_response.json()
        lat, lon = geo_data[0]['lat'], geo_data[0]['lon']
        
        # Get weather forecast
        weather_url = "http://api.openweathermap.org/data/2.5/forecast"
        weather_params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
        weather_response = requests.get(weather_url, params=weather_params, timeout=10)
        
        if weather_response.status_code == 200:
            data = weather_response.json()
            forecasts = []
            seen_dates = set()
            
            for item in data['list'][:40]:
                dt = datetime.fromtimestamp(item['dt'])
                date_str = dt.strftime('%Y-%m-%d')
                
                if date_str not in seen_dates and dt.hour in [12, 13, 14, 15]:
                    seen_dates.add(date_str)
                    forecasts.append({
                        "date": date_str,
                        "day": dt.strftime('%A'),
                        "temperature": round(item['main']['temp'], 1),
                        "feels_like": round(item['main']['feels_like'], 1),
                        "condition": item['weather'][0]['description'].title(),
                        "humidity": item['main']['humidity'],
                        "wind_speed": round(item['wind']['speed'], 1)
                    })
                
                if len(forecasts) == 5:
                    break
            
            return json.dumps({
                "city": city,
                "country": geo_data[0].get('country', 'Unknown'),
                "forecasts": forecasts
            })
        
        return json.dumps({"error": "Weather API error"})
    except Exception as e:
        return json.dumps({"error": str(e)})