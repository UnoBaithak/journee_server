from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional

class ItineraryGenerationRequestModel(BaseModel):
    destination: str
    num_days: int
    preferences: str

class ItineraryUpdationRequestModel(BaseModel):
    user_input: str
    itinerary_id: str
    day_id: Optional[str]
