from datetime import datetime
from services.db_service import DBService
from llm.llm_service import LLMService
from bson import ObjectId

class ItineraryUpdater:
    """Worker class to handle itinerary updates"""

    def __init__(self):
        self.collection = DBService().get_collection("itineraries")
        self.llm_service = LLMService()

    ### 🚀 Update Full Itinerary
    async def update_full(self, itinerary_id: str) -> (bool, str):
        itinerary = self.collection.find_one(itinerary_id)

        if not itinerary:
            return False, "Itinerary not found"




        

    ### 🚀 Update Single Day
    async def update_single_day(self, day_id: str, itinerary_id: str) -> bool:
        """Dummy method to replace single day details (Mocked for now)"""

        # 🔥 Mock updated day details
        updated_day = {
            "day_id": day_id,
            "activities": [
                {"name": "Morning Yoga", "time": "8:00 AM", "duration": 60, "category": "wellness"},
                {"name": "Explore Historical Museum", "time": "11:00 AM", "duration": 120, "category": "sightseeing"}
            ],
            "accommodation": {
                "hotel_name": "Heritage Inn",
                "check_in": datetime.utcnow().isoformat(),
                "check_out": datetime.utcnow().isoformat()
            }
        }

        itinerary = self.collection.find_one({"_id": ObjectId(itinerary_id)})

        itinerary["details"][day_id] = updated_day
        result = self.collection.update_one({"_id": ObjectId(itinerary_id)}, {"$set": {"details": itinerary["details"]}})

        if result.modified_count == 0:
            return False
        
        return True