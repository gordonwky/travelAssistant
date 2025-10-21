from typing import Any, Dict
from models.travel_model import TravelState

def format_travel_state_response(travel_state: TravelState) -> Dict[str, Any]:

    if hasattr(travel_state, "model_dump"):
        state = travel_state.model_dump()
    elif hasattr(travel_state, "dict"):
        state = travel_state.dict()
    else:
        state = dict(travel_state)

    meta = {
        "origin": state.get("origin"),
        "destination": state.get("destination"),
        "departure_date": state.get("departure_date"),
        "return_date": state.get("return_date")
    }

    response = {
        "flight": state.get("flight"),
        "hotel": state.get("hotel"),
        "itinerary": state.get("itinerary"),
        "dining": state.get("dining")
    }

    return response
