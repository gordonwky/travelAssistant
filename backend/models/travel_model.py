from typing import Annotated, TypedDict, List
from pydantic import Field
from langgraph.graph.message import add_messages
import operator
# import data models
from models.hotel_model import HotelItinerary
from models.flight_model import FlightResult
from models.itinerary_model import SpotList
from models.dining_model import DiningList
class TravelState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str = Field(description="Unique identifier for the user")
    origin: str = Field(description="the origin")
    destination: str = Field(description="the destination")
    departure_date: str = Field(description="Departure date in ISO 8601 format")
    return_date: str = Field(description="Return date in ISO 8601 format")
    itinerary: SpotList = Field(description="List of spots in the itinerary")
    dining: DiningList = Field(description="List of dining options")
    flight: FlightResult = Field(description="Flight information")
    hotel: HotelItinerary = Field(description="Hotel information")
    aggregate: Annotated[list, operator.add]