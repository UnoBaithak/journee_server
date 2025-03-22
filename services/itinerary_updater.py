from datetime import datetime
from typing import Dict
from services.db_service import DBService
from bson import ObjectId

class ItineraryUpdater:
    """Worker class to handle itinerary updates"""

    def __init__(self, user_input: str, itinerary_id: str):
        self.user_input = user_input
        self.itinerary_id = itinerary_id
        self.collection = DBService().get_collection("itineraries")

    ### 🚀 Update Full Itinerary
    async def update_full(self) -> bool:
        """Dummy method to replace full itinerary (Mocked for now)"""

        # 🔥 Mock updated itinerary
        updated_itinerary = {
            "metadata": {
                "destination": "Goa",
                "num_days": 3,
                "preferences": {"budget": "mid", "mood": "relax"}
            },
            "details": {
                "day_1": {
                    "day_id": "day_1",
                    "activities": [
                        {"name": "Sunset Beach Walk", "time": "5:00 PM", "duration": 60, "category": "leisure"},
                        {"name": "Dinner at Local Cafe", "time": "7:00 PM", "duration": 90, "category": "food"}
                    ],
                    "accommodation": {
                        "hotel_name": "Goa Beach Resort",
                        "check_in": datetime.utcnow().isoformat(),
                        "check_out": datetime.utcnow().isoformat()
                    }
                }
            },
            "status": "updated",
            "updated_at": datetime.utcnow().isoformat()
        }

        result = self.collection.update_one({"_id": ObjectId(self.itinerary_id)}, {"$set": updated_itinerary})

        if result.modified_count == 0:
            return False

        return True

    ### 🚀 Update Single Day
    async def update_single_day(self, day_id: str) -> bool:
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

        itinerary = self.collection.find_one({"_id": ObjectId(self.itinerary_id)})

        itinerary["details"][day_id] = updated_day
        result = self.collection.update_one({"_id": ObjectId(self.itinerary_id)}, {"$set": {"details": itinerary["details"]}})

        if result.modified_count == 0:
            return False
        
        return True