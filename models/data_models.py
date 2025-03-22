from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class Activity(BaseModel):
    name: str
    time: datetime
    duration: int
    category: str
    metadata: Optional[Dict[str, Any]] = None

class Accommodation(BaseModel):
    hotel_name: str
    check_in: datetime
    check_out: datetime
    metadata: Optional[Dict[str, Any]] = None

class DayDetails(BaseModel):
    day_id: str  # Unique ID for the day
    activities: List[Activity]
    accommodation: Optional[Accommodation]

class ItineraryMetadata(BaseModel):
    destination: str
    num_days: int
    preferences: dict

class Itinerary(BaseModel):
    metadata: ItineraryMetadata
    details: Dict[str, DayDetails]  # Mapping day to DayDetails
    created_at: datetime
    updated_at: datetime

class PointOfInterest(BaseModel):
    name: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None