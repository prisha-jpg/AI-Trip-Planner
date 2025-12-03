"""FastAPI application setup."""

from fastapi import FastAPI
from config.settings import settings
from models.schemas import (
    TripRequest, WeatherRequest, AttractionRequest,
    HotelRequest, CurrencyRequest, NearbyPlacesRequest
)
from . import routes

def create_app():
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION
    )
    
    # Add routes
    app.get("/")(routes.root)
    app.post("/plan-trip")(routes.plan_trip)
    app.get("/trip/{trip_id}")(routes.get_trip)
    app.get("/trip/{trip_id}/export")(routes.export_trip)
    app.post("/weather")(routes.get_weather)
    app.post("/attractions")(routes.get_attractions)
    app.post("/hotels")(routes.get_hotels)
    app.post("/currency")(routes.get_currency)
    app.post("/nearby-places")(routes.get_nearby)
    app.get("/health")(routes.health_check)
    
    return app