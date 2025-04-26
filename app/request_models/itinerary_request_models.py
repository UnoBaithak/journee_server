from pydantic import BaseModel
from typing import Optional

class ItineraryGenerationRequestModel(BaseModel):
    destination: Optional[str]
    num_days: Optional[int]
    preferences: Optional[str]
    user_input: Optional[str] = None
    user_id: Optional[str] = None

    def __str__(self):
        if self.user_input:
            return self.user_input
        else:
            return f"I want to travel to {self.destination} for {self.num_days} day(s)" + \
                    f". Help me plan an itinerary with the following notes: {self.preferences}"

class ItineraryUpdationRequestModel(BaseModel):
    user_id: Optional[str] = None
    user_input: str
    conversation_id: str
    itinerary_id: Optional[str] = None
    day_id: Optional[str] = None
