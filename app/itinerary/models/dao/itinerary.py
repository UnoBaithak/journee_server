from pydantic import BaseModel
from typing import List
from .day_details import DayDetails
from datetime import datetime

# Metadata about the itinerary
# destination - num_days - preference - creatorId - conversationId - clonedFrom (in case this itinerary is cloned)
class ItineraryMetadata(BaseModel):
    destination: str
    num_days: int
    preferences: str
    creatorId: str | None
    conversationId: str | None
    clonedFrom: str | None

class Itinerary(BaseModel):
    metadata: ItineraryMetadata
    title: str
    details: List[DayDetails]
    created_at: datetime
    updated_at: datetime