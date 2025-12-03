"""Pydantic models for API requests and responses."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from langgraph.graph import MessagesState

class TripRequest(BaseModel):
    from_city: str = Field(..., description="Origin city")
    to_city: str = Field(..., description="Destination city")
    arrival_date: str = Field(..., description="Arrival date in YYYY-MM-DD format")
    num_days: int = Field(..., ge=1, le=30, description="Number of days for the trip")
    arrival_time: str = Field(default="10:00 AM", description="Arrival time")
    num_adults: int = Field(..., ge=1, description="Number of adults")
    num_kids: int = Field(default=0, ge=0, description="Number of children")

class WeatherRequest(BaseModel):
    city: str
    date: Optional[str] = None

class AttractionRequest(BaseModel):
    city: str
    num_days: int = 3

class HotelRequest(BaseModel):
    city: str
    num_adults: int
    num_kids: int
    num_days: int

class CurrencyRequest(BaseModel):
    from_city: str
    to_city: str

class NearbyPlacesRequest(BaseModel):
    city: str

class TripPlannerState(MessagesState):
    """State class for the trip planner workflow."""
    from_city: str = ""
    to_city: str = ""
    arrival_date: str = ""
    num_days: int = 3
    arrival_time: str = "10:00 AM"
    num_adults: int = 2
    num_kids: int = 0
    weather_data: dict = {}
    attractions_data: dict = {}
    hotel_data: dict = {}
    currency_info: str = ""
    nearby_places_data: dict = {}
    itinerary: str = ""
    expenses_data: dict = {}