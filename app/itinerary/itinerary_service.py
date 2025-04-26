from services import DBService
from itinerary.models import Itinerary, DayDetails
from bson import ObjectId
from fastapi import HTTPException

class ItineraryService:

    def __init__(self):
        self.collection = DBService().get_collection("itineraries")

    def create_new_itinerary(self, itinerary: Itinerary):
        itinerary.is_temp = True
        result = self.collection.insert_one(itinerary.model_dump())
        return str(result.inserted_id)
    
    def update_itinerary(self, itinerary_id: str, day_id: str, updated_day_details: DayDetails):
        pass

    def get_itinerary(self, itinerary_id: str):
        itinerary = self.collection.find_one({"_id": ObjectId(itinerary_id)})

        if itinerary is None:
            raise HTTPException(status_code= 404, detail="Itinerary does not exist")
        
        return itinerary