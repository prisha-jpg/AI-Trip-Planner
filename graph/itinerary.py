"""Itinerary and expense calculation nodes."""

import pandas as pd
from models.schemas import TripPlannerState
from llm.config import llm

def create_itinerary_node(state: TripPlannerState):
    """Create a detailed itinerary based on collected data."""
    weather_text = str(pd.DataFrame(state.get("weather_data", {}).get("forecasts", []))) if state.get("weather_data") else "No data"
    attractions_text = str(pd.DataFrame(state.get("attractions_data", {}).get("items", []))) if state.get("attractions_data") else "No data"
    hotels_text = str(pd.DataFrame(state.get("hotel_data", {}).get("items", []))) if state.get("hotel_data") else "No data"
    nearby_text = str(pd.DataFrame(state.get("nearby_places_data", {}).get("items", []))) if state.get("nearby_places_data") else "No data"
    
    prompt = f"""Create a comprehensive travel itinerary:

TRIP DETAILS:
- From: {state['from_city']} → To: {state['to_city']}
- Arrival: {state['arrival_date']} at {state['arrival_time']}
- Duration: {state['num_days']} days
- Travelers: {state['num_adults']} adults, {state['num_kids']} children

WEATHER FORECAST: {weather_text}
TOP ATTRACTIONS: {attractions_text}
HOTELS: {hotels_text}
CURRENCY: {state.get('currency_info', 'No info')}
NEARBY PLACES: {nearby_text}

Create a detailed day-by-day itinerary with activities, meal suggestions, transportation tips, and packing recommendations."""
    
    try:
        response = llm.invoke(prompt)
        return {"itinerary": response.content}
    except Exception as e:
        return {"itinerary": f"Error: {str(e)}"}

def calculate_expenses_node(state: TripPlannerState):
    """Calculate detailed expense breakdown."""
    num_days = state.get("num_days", 3)
    num_adults = state.get("num_adults", 2)
    num_kids = state.get("num_kids", 0)
    expenses = []
    currency = "USD"
    
    # Accommodation
    if state.get("hotel_data") and "items" in state["hotel_data"]:
        hotels = state["hotel_data"]["items"]
        if hotels:
            hotel = hotels[min(2, len(hotels) - 1)]
            hotel_price = hotel.get('total_price', 150 * num_days)
            currency = hotel.get('currency', 'USD')
            expenses.append({
                "category": "Accommodation",
                "description": f"{hotel.get('name', 'Hotel')} - {num_days} nights",
                "amount": hotel_price,
                "currency": currency
            })
    
    if not expenses:
        expenses.append({
            "category": "Accommodation",
            "description": f"Estimated hotel - {num_days} nights",
            "amount": 150 * num_days,
            "currency": currency
        })
    
    # Attractions
    if state.get("attractions_data") and "items" in state["attractions_data"]:
        attractions = state["attractions_data"]["items"]
        total_attractions = sum([a.get('ticket_price', 0) for a in attractions]) * (num_adults + num_kids * 0.5)
        if attractions:
            currency = attractions[0].get('currency', currency)
        expenses.append({
            "category": "Attractions & Activities",
            "description": f"Entry tickets for {len(attractions)} attractions",
            "amount": round(total_attractions, 2),
            "currency": currency
        })
    else:
        expenses.append({
            "category": "Attractions & Activities",
            "description": "Estimated costs",
            "amount": 200,
            "currency": currency
        })
    
    # Food
    food_cost = 50 * (num_adults + num_kids) * num_days
    expenses.append({
        "category": "Food & Dining",
        "description": f"{num_adults + num_kids} people × {num_days} days",
        "amount": food_cost,
        "currency": currency
    })
    
    # Transportation
    transport_cost = 30 * num_days
    expenses.append({
        "category": "Local Transportation",
        "description": f"Metro, taxis - {num_days} days",
        "amount": transport_cost,
        "currency": currency
    })
    
    # Miscellaneous
    total_so_far = sum([e['amount'] for e in expenses])
    misc_cost = round(total_so_far * 0.1, 2)
    expenses.append({
        "category": "Miscellaneous",
        "description": "Souvenirs, tips (10%)",
        "amount": misc_cost,
        "currency": currency
    })
    
    # Total
    total_amount = round(sum([e['amount'] for e in expenses]), 2)
    expenses.append({
        "category": "TOTAL",
        "description": "Total estimated expenses",
        "amount": total_amount,
        "currency": currency
    })
    
    return {"expenses_data": {"items": expenses, "currency": currency, "total": total_amount}}