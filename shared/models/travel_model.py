from typing import Annotated, TypedDict
from pydantic import Field
# from langgraph.graph.message import add_messages
# import data models
class TravelRequest(TypedDict):
    # user_id: str
    origin: str
    destination: str
    departure_date: str
    return_date: str
    # messages: Annotated[list, add_messages]