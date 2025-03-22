from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class ItineraryGenerationRequestModel(BaseModel):
    destination: str
    num_days: int
    preferences: Dict[str, Any]

class ItineraryUpdationRequestModel(BaseModel):
    user_input: str
