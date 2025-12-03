"""Trip planner workflow graph."""

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from models.schemas import TripPlannerState
from tools.all_tools import all_tools
from .nodes import agent_node, should_continue, process_results_node
from .itinerary import create_itinerary_node, calculate_expenses_node

def create_workflow():
    """Create and compile the trip planner workflow."""
    # Build workflow
    workflow = StateGraph(TripPlannerState)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(all_tools))
    workflow.add_node("process_results", process_results_node)
    workflow.add_node("create_itinerary", create_itinerary_node)
    workflow.add_node("calculate_expenses", calculate_expenses_node)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add edges
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", "process_results": "process_results"})
    workflow.add_edge("tools", "agent")
    workflow.add_edge("process_results", "create_itinerary")
    workflow.add_edge("create_itinerary", "calculate_expenses")
    workflow.add_edge("calculate_expenses", END)
    
    # Compile with memory
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

# Create the compiled workflow
app_graph = create_workflow()