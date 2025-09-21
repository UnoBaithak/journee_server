from pydantic import BaseModel
from .activity import Activity
from typing import List

class DayDetails(BaseModel):
    day_id: int
    activities: List[Activity]