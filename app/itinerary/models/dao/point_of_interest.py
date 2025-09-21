from pydantic import BaseModel, Field
from typing import Optional

class PointOfInterest(BaseModel):
    name: str = Field(description="Name of the point of interest being visited")
    lat: Optional[float] = Field(default=None, description="Latitude of the point of interest.")
    lon: Optional[float] = Field(default=None, description="Longitude of the point of interest.")
    category: Optional[str] = Field(default=None, description="Category of the point of interest.")
    description: Optional[str] = Field(default=None, description="Description of the point of interest.")
    website: Optional[str] = Field(default=None, description="Website of the point of interest.")
