# Define a tool
from langchain_core.tools import tool
from typing import List
from models.hotel_model import HotelItem, HotelItinerary
from langgraph.types import Command
from langchain_core.messages import ToolMessage
@tool
def hotel_search(city: str) -> Command:
    """Pretend API call for finding hotel in a given city"""

    hotels_data = [
        {
            "hotel_name": "Hotel Tou Nishinotoin Tokyo",
            "location": "123 Nishinotoin, Tokyo",
            "check_in_date": "2024-07-01",
            "check_out_date": "2024-07-05",
            "price": 180.0,
            "currency": "JPY",
            "rating": 4.8,
        },
        {
            "hotel_name": "Tokyo Royal Hotel",
            "location": "456 Royal St, Tokyo",
            "check_in_date": "2024-07-01",
            "check_out_date": "2024-07-05",
            "price": 150.0,
            "currency": "JPY",
            "rating": 4.7,
        },
        {
            "hotel_name": "Tokyo Garden Palace",
            "location": "789 Garden Ave, Tokyo",
            "check_in_date": "2024-07-01",
            "check_out_date": "2024-07-05",
            "price": 130.0,
            "currency": "JPY",
            "rating": 4.6,
        },
    ]

    # Convert to HotelItem model instances
    top_hotels: List[HotelItem] = [HotelItem(**hotel) for hotel in hotels_data]
    return Command(update={
        "hotel": HotelItinerary(hotels=top_hotels),
    })


