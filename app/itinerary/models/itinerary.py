from pydantic import BaseModel
from typing import List
from .day_details import DayDetails
from datetime import datetime

class ItineraryMetadata(BaseModel):
    destination: str
    num_days: int
    preferences: str
    creatorId: str | None
    conversationId: str | None
    clonedFrom: str | None

# We are not linking itinerary to conversation, because itinerary is stateless relative to conversation
# Conversation is instead linked to an itinerary because each conversation is unique.  
# This lets a user share itinerary without bringing the separate user into conversation
# Group conversation could be a new feature, which can be implemented in this architecture, multiple users
# will have the same conversation id in their list of conversations and they can edit individually. 
# For combined / edits, we will need to think.. but i believe the current model can carry it. 
class Itinerary(BaseModel):
    metadata: ItineraryMetadata
    title: str
    details: List[DayDetails]
    created_at: datetime
    updated_at: datetime