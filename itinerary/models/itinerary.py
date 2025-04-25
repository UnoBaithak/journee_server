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

    @staticmethod
    def create_placeholder_itinerary(num_days: int, destination: str, preferences: str):
        metadata = ItineraryMetadata()
        metadata.num_days = num_days
        metadata.destination = destination
        metadata.preferences = preferences

        itinerary = Itinerary()
        itinerary.created_at = datetime.now()
        itinerary.updated_at = datetime.now()
        itinerary.title = ""
        itinerary.metadata = metadata
        itinerary.details = []

        return itinerary