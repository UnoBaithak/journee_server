from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .point_of_interest import PointOfInterest

class Activity(BaseModel):
    activity_id: str = Field(description="Unique identifier for the activity.")
    pois: Optional[List[PointOfInterest]] = Field(description="List of points of interest/hotspots being visited in this activity.")
    title: str = Field(description="Title of the activity.")
    time: str = Field(description="Date and time the activity is scheduled for.")
    duration: int = Field(description="Duration of the activity in minutes.")
    category: str = Field(description="Category of the activity.")
    description: str = Field(description="Detailed description of the activity.")
