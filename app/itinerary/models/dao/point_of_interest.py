from pydantic import BaseModel, Field
from typing import Optional

class PointOfInterest(BaseModel):
    name: str = Field(description="Name of the point of interest being visited")
    lat: Optional[float] = None
    lon: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None