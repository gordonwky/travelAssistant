from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage
from models.travel_model import TravelState
from models.flight_model import FlightResult
from config.llm_models import llm
def flight_agent(state: TravelState):
    """
    Generates a draft flight itinerary based on origin, destination and dates.
    Uses an LLM bound with search tools (e.g., search_spots).
    """

    # Bind tools (e.g., search spots, local attractions)
    # model_with_tools = llm.bind_tools([search_spots])
    model_with_tools = llm.with_structured_output(FlightResult)
    # Extract info from state
    origin = state["origin"]
    destination = state["destination"]
    departure_date = state["departure_date"]
    return_date = state["return_date"]
    # Create prompt for itinerary planning
    system_prompt = f"""
    You are an expert travel assistant specializing in flight planning.
    Given the user's departure location {origin}, destination '{destination}', and travel dates '{departure_date}' to '{return_date}', 
    generate a detailed round-trip flight itinerary. Your response should include:

    - Multiple flight options (if available)
    - Airline name
    - Flight number
    - Departure and arrival airports (IATA codes)
    - Departure and arrival times (ISO 8601 format)
    - Return flight details (departure and arrival times in ISO 8601 format)
    - Total price for the round trip and currency code
    - Seat class (e.g., Economy, Business)
    - Number of stops for the round trip
    - Total duration of the round trip
    - Layover times and locations (if applicable)

    Present the information in a clear, structured format suitable for further processing.
    You could fake one for testing purposes.
    """

    # Invoke model
    result = model_with_tools.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Please arrange my flight from {origin} to {destination} from {departure_date} to {return_date}."}
    ])
    print("Flight Result:", result)
    # Return updated state with draft flight information
    # state["flight"] = result
    # could be raw LLM output or structured JSON if you parse it
    return {"flight": result}
