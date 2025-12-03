"""Currency conversion tools."""

import json
import requests
from langchain.tools import tool

@tool
def convert_currency(from_city: str, to_city: str) -> str:
    """Get currency conversion information."""
    city_to_currency = {
        # United States
        "new york": "USD", "los angeles": "USD", "chicago": "USD", "san francisco": "USD",
        "boston": "USD", "seattle": "USD", "miami": "USD", "las vegas": "USD", "philadelphia": "USD",
        "washington": "USD", "atlanta": "USD", "denver": "USD", "phoenix": "USD", "detroit": "USD",
        
        # India
        "mumbai": "INR", "delhi": "INR", "bangalore": "INR", "chennai": "INR", "kolkata": "INR",
        "hyderabad": "INR", "pune": "INR", "ahmedabad": "INR", "surat": "INR", "jaipur": "INR",
        "lucknow": "INR", "kanpur": "INR", "nagpur": "INR", "indore": "INR", "thane": "INR",
        "bhopal": "INR", "visakhapatnam": "INR", "pimpri-chinchwad": "INR", "patna": "INR",
        "vadodara": "INR", "ghaziabad": "INR", "ludhiana": "INR", "agra": "INR", "nashik": "INR",
        "faridabad": "INR", "meerut": "INR", "rajkot": "INR", "kalyan-dombivali": "INR",
        "vasai-virar": "INR", "varanasi": "INR", "srinagar": "INR", "aurangabad": "INR",
        "dhanbad": "INR", "amritsar": "INR", "navi mumbai": "INR", "allahabad": "INR",
        "howrah": "INR", "ranchi": "INR", "gwalior": "INR", "jabalpur": "INR", "coimbatore": "INR",
        
        # United Kingdom
        "london": "GBP", "manchester": "GBP", "edinburgh": "GBP", "birmingham": "GBP",
        "liverpool": "GBP", "bristol": "GBP", "glasgow": "GBP", "leeds": "GBP",
        
        # European Union
        "paris": "EUR", "berlin": "EUR", "rome": "EUR", "madrid": "EUR", "barcelona": "EUR",
        "amsterdam": "EUR", "vienna": "EUR", "brussels": "EUR", "milan": "EUR", "munich": "EUR",
        "prague": "EUR", "budapest": "EUR", "warsaw": "EUR", "dublin": "EUR", "helsinki": "EUR",
        
        # Other countries
        "tokyo": "JPY", "osaka": "JPY", "kyoto": "JPY", "yokohama": "JPY",
        "singapore": "SGD", "dubai": "AED", "abu dhabi": "AED",
        "sydney": "AUD", "melbourne": "AUD", "brisbane": "AUD", "perth": "AUD",
        "toronto": "CAD", "vancouver": "CAD", "montreal": "CAD", "calgary": "CAD",
        "beijing": "CNY", "shanghai": "CNY", "guangzhou": "CNY", "shenzhen": "CNY",
        "moscow": "RUB", "st petersburg": "RUB",
        "sao paulo": "BRL", "rio de janeiro": "BRL",
        "mexico city": "MXN", "guadalajara": "MXN",
        "cairo": "EGP", "lagos": "NGN", "johannesburg": "ZAR", "cape town": "ZAR"
    }
    
    def get_currency_for_city(city_name):
        """Get currency for a city with fallback logic."""
        city_lower = city_name.lower()
        
        # Direct lookup first
        if city_lower in city_to_currency:
            return city_to_currency[city_lower]
        
        # Fallback patterns for common countries
        indian_patterns = ['nagar', 'abad', 'pur', 'ganj', 'garh', 'kota', 'puram']
        us_patterns = ['ville', 'ton', 'burg', 'field', 'wood', 'land', 'city']
        
        # Check if city name suggests Indian city
        for pattern in indian_patterns:
            if pattern in city_lower:
                return "INR"
        
        # Check if city name suggests US city  
        for pattern in us_patterns:
            if pattern in city_lower:
                return "USD"
        
        # Default fallback
        return "USD"
    
    from_curr = get_currency_for_city(from_city)
    to_curr = get_currency_for_city(to_city)
    
    if from_curr == to_curr:
        return json.dumps({
            "from_city": from_city, "to_city": to_city,
            "from_currency": from_curr, "to_currency": to_curr,
            "exchange_rate": 1.0, "message": f"Both cities use {from_curr}"
        })
    
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            rate = data['rates'].get(to_curr, 1.0)
            return json.dumps({
                "from_city": from_city, "to_city": to_city,
                "from_currency": from_curr, "to_currency": to_curr,
                "exchange_rate": round(rate, 4),
                "message": f"1 {from_curr} = {rate:.4f} {to_curr}"
            })
        return json.dumps({"error": "API unavailable"})
    except Exception as e:
        return json.dumps({"error": str(e)})