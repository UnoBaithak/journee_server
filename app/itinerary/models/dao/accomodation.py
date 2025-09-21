from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class BudgetEnum(str, Enum):
    BUDGET = "Budget"
    MID_RANGE = "Mid-range"
    LUXURY = "Luxury"

class Accommodation(BaseModel):
    hotel_name: str = Field(description="Name of the hotel or lodging.")
    check_in: str = Field(description="Check-in date and time.")
    check_out: str = Field(description="Check-out date and time.")
    budget: BudgetEnum = Field(description="Budget classification for the accommodation.")
