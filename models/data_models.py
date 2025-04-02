from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class PointOfInterest(BaseModel):
    name: str = Field(description="Name of the point of interest being visited")
    lat: Optional[float] = None
    lon: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None

class Activity(BaseModel):
    activity_id: str
    pois: Optional[List[PointOfInterest]] = Field(description="List of points of interest/hotspots being visited in this activity.")
    title: str
    time: datetime
    duration: int
    category: str
    description: str
    # metadata: Dict[str, Any] = Field(description="Placeholder, always return None")

class Accommodation(BaseModel):
    hotel_name: str
    check_in: datetime
    check_out: datetime
    metadata: Optional[Dict[str, Any]] = None

class DayDetails(BaseModel):
    day_id: str 
    activities: List[Activity]

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