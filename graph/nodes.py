"""Graph nodes for the trip planner workflow."""

import json
import pandas as pd
from models.schemas import TripPlannerState
from llm.config import get_llm_with_tools
from tools.all_tools import all_tools

# Get LLM with tools
llm_with_tools = get_llm_with_tools(all_tools)

def agent_node(state: TripPlannerState):
    """Main agent node that processes requests and calls tools."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: TripPlannerState):
    """Determine whether to continue with tools or process results."""
    messages = state["messages"]
    last_message = messages[-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    return "process_results"

def process_results_node(state: TripPlannerState):
    """Process the results from tool calls and organize data."""
    messages = state["messages"]
    weather_data = attractions_data = hotels_data = currency_data = nearby_data = None
    
    for msg in messages:
        if hasattr(msg, '__class__') and msg.__class__.__name__ == 'ToolMessage':
            try:
                content = json.loads(msg.content)
                if "forecasts" in content:
                    weather_data = content
                elif isinstance(content, list) and len(content) > 0:
                    if "ticket_price" in content[0]:
                        attractions_data = {"items": content}
                    elif "star_rating" in content[0]:
                        hotels_data = {"items": content}
                    elif "distance_km" in content[0]:
                        nearby_data = {"items": content}
                elif "exchange_rate" in content:
                    currency_data = content
            except:
                continue
    
    currency_str = ""
    if currency_data:
        currency_str = f"""Currency Conversion:
From: {currency_data.get('from_currency', 'N/A')} ({currency_data.get('from_city', 'N/A')})
To: {currency_data.get('to_currency', 'N/A')} ({currency_data.get('to_city', 'N/A')})
Exchange Rate: 1 {currency_data.get('from_currency', '')} = {currency_data.get('exchange_rate', 0)} {currency_data.get('to_currency', '')}"""
    
    return {
        "weather_data": weather_data or {},
        "attractions_data": attractions_data or {},
        "hotel_data": hotels_data or {},
        "currency_info": currency_str,
        "nearby_places_data": nearby_data or {}
    }