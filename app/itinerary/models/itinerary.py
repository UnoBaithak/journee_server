from pydantic import BaseModel
from typing import List
from .day_details import DayDetails
from datetime import datetime

class ItineraryMetadata(BaseModel):
    destination: str
    num_days: int
    preferences: str

class Itinerary(BaseModel):
    metadata: ItineraryMetadata
    title: str
    details: List[DayDetails]
    created_at: datetime
    updated_at: datetime