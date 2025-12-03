"""API routes for the travel planner."""

import json
import uuid
from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import FileResponse, JSONResponse
from langchain_core.messages import HumanMessage

from models.schemas import (
    TripRequest, WeatherRequest, AttractionRequest, 
    HotelRequest, CurrencyRequest, NearbyPlacesRequest
)
from tools.weather import get_weather_info
from tools.attractions import get_top_attractions, get_nearby_places
from tools.hotels import get_hotel_recommendations
from tools.currency import convert_currency
from utils.export import export_to_excel
from graph.workflow import app_graph

# Storage for trip plans
trip_plans = {}

async def root():
    """Root endpoint with API information."""
    return {
        "message": "AI Travel Planner API",
        "version": "1.0.0",
        "endpoints": {
            "POST /plan-trip": "Create a complete trip plan",
            "GET /trip/{trip_id}": "Get trip plan details",
            "GET /trip/{trip_id}/export": "Export trip plan to Excel",
            "POST /weather": "Get weather information",
            "POST /attractions": "Get top attractions",
            "POST /hotels": "Get hotel recommendations",
            "POST /currency": "Get currency conversion"
        }
    }

async def plan_trip(request: TripRequest):
    """Create a complete trip plan."""
    trip_id = str(uuid.uuid4())
    
    initial_message = f"""I need help planning a trip:
From: {request.from_city} → To: {request.to_city}
Arrival: {request.arrival_date} at {request.arrival_time}
Duration: {request.num_days} days
Travelers: {request.num_adults} adults, {request.num_kids} children

Get weather forecast, top attractions, hotels, currency conversion, and nearby places."""
    
    initial_state = {
        "messages": [HumanMessage(content=initial_message)],
        "from_city": request.from_city,
        "to_city": request.to_city,
        "arrival_date": request.arrival_date,
        "num_days": request.num_days,
        "arrival_time": request.arrival_time,
        "num_adults": request.num_adults,
        "num_kids": request.num_kids
    }
    
    config = {"configurable": {"thread_id": trip_id}}
    
    try:
        final_state = None
        for output in app_graph.stream(initial_state, config):
            node_name = list(output.keys())[0]
            if final_state is None:
                final_state = output[node_name]
            else:
                final_state.update(output[node_name])
        
        # Store trip plan
        trip_plans[trip_id] = final_state
        
        return {
            "trip_id": trip_id,
            "status": "completed",
            "summary": {
                "from": request.from_city,
                "to": request.to_city,
                "duration": f"{request.num_days} days",
                "travelers": f"{request.num_adults} adults, {request.num_kids} kids"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_trip(trip_id: str):
    """Get complete trip plan details."""
    if trip_id not in trip_plans:
        raise HTTPException(status_code=404, detail="Trip plan not found")
    
    state = trip_plans[trip_id]
    return {
        "trip_id": trip_id,
        "trip_details": {
            "from_city": state.get("from_city"),
            "to_city": state.get("to_city"),
            "arrival_date": state.get("arrival_date"),
            "num_days": state.get("num_days")
        },
        "weather": state.get("weather_data"),
        "attractions": state.get("attractions_data"),
        "hotels": state.get("hotel_data"),
        "currency": state.get("currency_info"),
        "nearby_places": state.get("nearby_places_data"),
        "itinerary": state.get("itinerary"),
        "expenses": state.get("expenses_data")
    }

async def export_trip(trip_id: str):
    """Export trip plan to Excel file."""
    if trip_id not in trip_plans:
        raise HTTPException(status_code=404, detail="Trip plan not found")
    
    state = trip_plans[trip_id]
    filename = f"trip_plan_{trip_id}.xlsx"
    
    try:
        export_to_excel(state, filename)
        return FileResponse(
            filename,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            filename=filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_weather(request: WeatherRequest):
    """Get weather information for a city."""
    result = get_weather_info.invoke({"city": request.city, "date": request.date})
    return JSONResponse(content=json.loads(result))

async def get_attractions(request: AttractionRequest):
    """Get top attractions for a city."""
    result = get_top_attractions.invoke({"city": request.city, "num_days": request.num_days})
    return JSONResponse(content=json.loads(result))

async def get_hotels(request: HotelRequest):
    """Get hotel recommendations."""
    result = get_hotel_recommendations.invoke({
        "city": request.city,
        "num_adults": request.num_adults,
        "num_kids": request.num_kids,
        "num_days": request.num_days
    })
    return JSONResponse(content=json.loads(result))

async def get_currency(request: CurrencyRequest):
    """Get currency conversion information."""
    result = convert_currency.invoke({"from_city": request.from_city, "to_city": request.to_city})
    return JSONResponse(content=json.loads(result))

async def get_nearby(request: NearbyPlacesRequest):
    """Get nearby places to visit."""
    result = get_nearby_places.invoke({"city": request.city})
    return JSONResponse(content=json.loads(result))

async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}