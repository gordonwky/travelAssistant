from typing import Annotated, List
from typing_extensions import TypedDict
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from config.llm_models import llm
from models.travel_model import TravelState
from models.dining_model import DiningList
from langchain_core.messages import ToolMessage
# @tool
# def search_spots():
#     pass

def dining_agent(state: TravelState):
    """
    Generates a draft dining plan based on itinerary and dates.
    Uses an LLM bound with search tools (e.g., search_dining).
    """

    # Bind tools (e.g., search spots, local attractions)
    # model_with_tools = llm.bind_tools([search_spots])
    model_with_tools = llm.with_structured_output(DiningList)
    # Extract info from state
    itinerary = state.get("itinerary", [])
    # Create prompt for dining planning
    system_prompt = f"""
    You are a Dining Planner AI.
    Based on the following itinerary:
    {itinerary}
    Suggest dining options for each day.
    Keep in mind travel time between spots and variety.
    """

    # Invoke model
    result = model_with_tools.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Please plan my dining for each day."}
    ])
    print("Dining Result:", result)
    # Return updated state with draft dining plan
    return {"dining": result}

