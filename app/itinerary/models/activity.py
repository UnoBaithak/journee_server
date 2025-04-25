from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .point_of_interest import PointOfInterest

class Activity(BaseModel):
    activity_id: str
    pois: Optional[List[PointOfInterest]] = Field(description="List of points of interest/hotspots being visited in this activity.")
    title: str
    time: datetime
    duration: int
    category: str
    description: str