from pydantic import BaseModel, Field
from typing import List
from .day_details import DayDetails
from datetime import datetime

# Metadata about the itinerary
# destination - num_days - preference - creatorId - conversationId - clonedFrom (in case this itinerary is cloned)
class ItineraryMetadata(BaseModel):
    destination: str = Field(description="The primary destination of the trip.")
    num_days: int = Field(description="The total number of days in the trip.")
    preferences: str = Field(description="User preferences for the itinerary.")
    creatorId: str | None = Field(default=None, description="ID of the user who created the itinerary.")
    conversationId: str | None = Field(default=None, description="ID of the conversation related to the itinerary.")
    clonedFrom: str | None = Field(default=None, description="ID of the itinerary this was cloned from.")

class Flight(BaseModel):
    start_date: datetime = Field(description="Start date and time of the flight.")
    travel_time: str = Field(description="Total travel time of the flight.")
    from_location: str = Field(description="Departure location of the flight.")
    to_location: str = Field(description="Arrival location of the flight.")

class Itinerary(BaseModel):
    metadata: ItineraryMetadata = Field(description="Metadata about the itinerary.")
    title: str = Field(description="Title of the itinerary.")
    details: List[DayDetails] = Field(description="List of day details for the itinerary.")
    flights: List[Flight] = Field(description="List of flights for the itinerary.")
    created_at: datetime = Field(description="Timestamp of when the itinerary was created.")
    updated_at: datetime = Field(description="Timestamp of when the itinerary was last updated.")
    response :str = Field(description="Response from the agent")