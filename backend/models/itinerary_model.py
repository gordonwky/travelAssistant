from pydantic import BaseModel, Field
from typing import List, Optional

class SpotItem(BaseModel):
    date: str = Field(description="Date of the itinerary in YYYY-MM-DD format")
    morning: Optional[str] = Field(default=None, description="Planned activity in the morning")
    afternoon: Optional[str] = Field(default=None, description="Planned activity in the afternoon")
    evening: Optional[str] = Field(default=None, description="Planned activity in the evening")
class SpotList(BaseModel):
    spots: List[SpotItem] = Field(description="List of spots in the itinerary")

