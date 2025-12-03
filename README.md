# AI Travel Planner - 

## Project Structure

```
AI-Trip-Planner/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── config/                 # Configuration and settings
│   ├── __init__.py
│   └── settings.py        # Environment variables and app settings
├── models/                 # Pydantic models and schemas
│   ├── __init__.py
│   └── schemas.py         # API request/response models
├── llm/                   # LLM configuration and initialization
│   ├── __init__.py
│   └── config.py          # ChatGroq LLM setup
├── tools/                 # LangChain tools for different functionalities
│   ├── __init__.py
│   ├── all_tools.py       # Tool collection and exports
│   ├── weather.py         # Weather API integration
│   ├── attractions.py     # Attraction and places tools
│   ├── hotels.py          # Hotel recommendation tools
│   └── currency.py        # Currency conversion tools
├── graph/                 # LangGraph workflow and nodes
│   ├── __init__.py
│   ├── workflow.py        # Graph definition and compilation
│   ├── nodes.py           # Core workflow nodes
│   └── itinerary.py       # Itinerary and expense calculation
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── export.py          # Excel export functionality
├── api/                   # FastAPI routes and application
│   ├── __init__.py
│   ├── app.py             # FastAPI app creation and setup
│   └── routes.py          # API endpoint implementations
└── notebooks/             # Jupyter notebooks
    └── travel-planner-assignment.ipynb
```

## Key Benefits of Modular Architecture

1. **Separation of Concerns**: Each module has a specific responsibility
2. **Maintainability**: Easier to modify and extend individual components
3. **Testability**: Components can be tested in isolation
4. **Reusability**: Modules can be imported and used across different parts
5. **Scalability**: New features can be added without affecting existing code

## Module Descriptions

### `config/`
- **settings.py**: Centralized configuration management with environment variables
- Handles API keys, LLM settings, and server configuration

### `models/`
- **schemas.py**: All Pydantic models for API requests/responses and state management
- Includes TripRequest, WeatherRequest, TripPlannerState, etc.

### `llm/`
- **config.py**: LLM initialization and configuration
- Provides functions to get LLM instances with or without tools

### `tools/`
- Individual tool files for different functionalities
- **weather.py**: OpenWeatherMap API integration
- **attractions.py**: Attraction recommendations using LLM
- **hotels.py**: Hotel recommendation tools
- **currency.py**: Currency conversion with exchange rate API
- **all_tools.py**: Centralized tool collection

### `graph/`
- **workflow.py**: LangGraph StateGraph definition and compilation
- **nodes.py**: Core workflow nodes (agent, tool routing, result processing)
- **itinerary.py**: Specialized nodes for itinerary creation and expense calculation

### `utils/`
- **export.py**: Excel export functionality with formatting
- Utility functions that can be shared across modules

### `api/`
- **app.py**: FastAPI application factory and setup
- **routes.py**: All API endpoint implementations
- Clean separation of web layer from business logic

## Running the Application

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in a `.env` file:
```
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
EXCHANGERATE_API_KEY=your_exchangerate_api_key
```

3. Run the application:
```bash
python main.py
```

The server will start on `http://0.0.0.0:8000`

## API Endpoints

- `POST /plan-trip` - Create a complete trip plan
- `GET /trip/{trip_id}` - Get trip plan details  
- `GET /trip/{trip_id}/export` - Export trip to Excel
- `POST /weather` - Get weather information
- `POST /attractions` - Get top attractions
- `POST /hotels` - Get hotel recommendations
- `POST /currency` - Get currency conversion
- `POST /nearby-places` - Get nearby places
- `GET /health` - Health check

## Next Steps

This modular structure makes it easy to:
- Add new tools by creating files in the `tools/` directory
- Extend the workflow by adding nodes in the `graph/` directory
- Add new API endpoints in the `api/` directory
- Modify configuration in the `config/` directory
- Add new data models in the `models/` directory