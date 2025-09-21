from pydantic import BaseModel, Field
from .activity import Activity
from typing import List, Optional
from .accomodation import Accommodation

class DayDetails(BaseModel):
    day_id: int = Field(description="The day number of the trip.")
    activities: List[Activity] = Field(description="List of activities scheduled for the day.")
    accommodation: Optional[Accommodation] = Field(default=None, description="Accommodation for the day.")