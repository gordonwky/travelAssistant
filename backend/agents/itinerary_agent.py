from langgraph.graph import StateGraph, START, END
from config.llm_models import llm
from models.travel_model import TravelState
from models.itinerary_model import SpotList
from agents.dining_agent import dining_agent
from agents.flight_agent import flight_agent
from agents.hotel_agent import hotel_agent
from langgraph.prebuilt import ToolNode, tools_condition 
from tools.hotel_tools import hotel_search
# @tool
# def search_spots():
#     pass

def itinerary_agent(state: TravelState):
    """
    Generates a draft itinerary based on destination and dates.
    Uses an LLM bound with search tools (e.g., search_spots).
    """

    # Bind tools (e.g., search spots, local attractions)
    # model_with_tools = llm.bind_tools([search_spots])
    model_with_tools = llm.with_structured_output(SpotList)
    # Extract info from state
    destination = state["destination"]
    departure_date = state["departure_date"]
    return_date = state["return_date"]
    flight = state["flight"]
    # Create prompt for itinerary planning
    system_prompt = f"""
    You are a Spots Planner AI.
    Based on the destination '{destination}' and dates '{departure_date} - {return_date}',
    consider the flight details: {flight}, save buffer travel time for the flight.
    Using this information, create a day-by-day itinerary draft.
    Suggest key attractions, districts, and activities for each day for morning, afternoon, and evening.
    Do not include any transportation details, dining suggestions, or accommodation recommendations.
    Keep in mind travel time between spots and variety.

    """

    # Invoke model
    result = model_with_tools.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Please plan my trip to {destination} from {departure_date} to {return_date}."}
    ])
    print("Itinerary Result:", result)
    # Return updated state with draft itinerary
    return {"itinerary": result}
    # could be raw LLM output or structured JSON if you parse it


