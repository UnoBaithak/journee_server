from models.request_models import ItineraryGenerationRequestModel
from models.data_models import Itinerary, ItineraryMetadata, Activity, DayDetails
from services.db_service import DBService
from datetime import datetime

class ItineraryGenerator():
    def __init__(self, itineraryGenerationRequest: ItineraryGenerationRequestModel):
        self.destination = itineraryGenerationRequest.destination
        self.num_days = itineraryGenerationRequest.num_days
        self.preferences = itineraryGenerationRequest.preferences
        self.collection = DBService().get_collection("itineraries")
    
    def generate_itinerary(self) -> Itinerary:
        """Generate a dummy itinerary with updated models"""

        dummy_details = {
            f"day_{i+1}": DayDetails(
                day_id=f"day_{i+1}_dummy",
                activities=[
                    Activity(
                        name="Explore Local Area Fiveeeeee",
                        time=datetime.utcnow().replace(hour=10, minute=0),  # ✅ 10:00 AM
                        duration=120,  # ✅ Duration in minutes (2 hours)
                        category="sightseeing"
                    ),
                    Activity(
                        name="Relax at a Cafe",
                        time=datetime.utcnow().replace(hour=13, minute=0),  # ✅ 1:00 PM
                        duration=90,  # ✅ Duration in minutes (1.5 hours)
                        category="food"
                    )
                ],
                accommodation=None
            )
            for i in range(self.num_days)
        }

        itinerary_metadata = ItineraryMetadata(
            destination=self.destination,
            num_days=self.num_days,
            preferences=self.preferences
        )

        itinerary = Itinerary(
            metadata=itinerary_metadata,
            details=dummy_details,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        return itinerary

    async def save_to_db(self, itinerary: Itinerary) -> str:
        """Insert itinerary into MongoDB and return generated ID"""
        itinerary_dict = itinerary.dict()
        result = self.collection.insert_one(itinerary_dict)
        return str(result.inserted_id)

    async def build_and_save(self) -> str:
        """Create, save, and return the itinerary ID"""
        itinerary = self.generate_itinerary()
        itinerary_id = await self.save_to_db(itinerary)
        return itinerary_id

    
