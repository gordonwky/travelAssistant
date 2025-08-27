from pydantic import BaseModel, Field
from typing import List


class RestaurantItem(BaseModel):
    restaurant_name: str = Field(description="Name of the restaurant")
    cuisine: str = Field(description="Type of cuisine (e.g., Italian, Chinese)")
    location: str = Field(description="Location of the restaurant")
    price_range: str = Field(description="Price range (e.g., $, $$, $$$)")
    rating: float = Field(description="Restaurant rating (e.g., 4.5)")

class DiningPlan(BaseModel):
    date: str = Field(description="Date of the dining plan in YYYY-MM-DD format")
    morning: RestaurantItem = Field(description="Recommended restaurants for breakfast")
    afternoon: RestaurantItem = Field(description="Recommended restaurants for lunch")
    evening: RestaurantItem = Field(description="Recommended restaurants for dinner")

class DiningList(BaseModel):
    meals: List[DiningPlan] = Field(description="List of dining plans for the day")
