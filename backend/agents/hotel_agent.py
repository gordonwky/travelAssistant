from tools.hotel_tools import hotel_search
from config.llm_models import llm
from models.travel_model import TravelState
from typing import List
# Create the agent


def hotel_agent(state: TravelState):
    """
    Generates a draft itinerary based on destination and dates.
    Uses an LLM bound with search tools (e.g., search_spots).
    """

    # Bind tools (e.g., search spots, local attractions)
    model_with_tools = llm.bind_tools([hotel_search])
    # Extract info from state
    itinerary = state['itinerary']

    # Create prompt for itinerary planning
    system_prompt = f"""
        "You are a hotel agent.\n\n"
        "You will be provided with a draft itinerary and you need to find hotels based on the itinerary.\n\n"
        f"ITINERARY:\n{itinerary}\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with hotel-related tasks, DO NOT do any job\n"
        "- After you're done with your tasks, update the to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    """

    # Invoke model
    result = model_with_tools.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Arrange hotels based on my itinerary."}
    ])
    # print("Hotel Search Result:", result)
    # Return updated state with draft itinerary
    # state["hotel"] = result  # could be raw LLM output or structured JSON if you parse it
    if hasattr(result, "tool_calls") and result.tool_calls:
        tool_call = result.tool_calls[0]  # assuming only one tool call
        city = tool_call["args"]["city"]
        command = hotel_search.invoke(city)       # returns Command(update={...})
        return command                       # LangGraph applies update automatically

    # Fallback: no tool call detected
    return {}


