from pydantic import BaseModel, Field
from typing import List
class HotelItem(BaseModel):
    hotel_name: str = Field(description="Name of the hotel")
    location: str = Field(description="Location of the hotel")
    check_in_date: str = Field(description="Check-in date in ISO 8601 format")
    check_out_date: str = Field(description="Check-out date in ISO 8601 format")
    price: float = Field(description="Price per night")
    currency: str = Field(description="Currency code for the price")
    rating: float = Field(description="Hotel rating (e.g., 4.5)")

class HotelItinerary(BaseModel):
    hotels: List[HotelItem] = Field(description="List of hotels in the itinerary")
