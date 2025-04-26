from services import DBService
from itinerary.models import Itinerary, DayDetails
from bson import ObjectId
from fastapi import HTTPException

class ItineraryService:

    def __init__(self):
        self.collection = DBService().get_collection("itineraries")

    def create_new_itinerary(self, itinerary: Itinerary):
        result = self.collection.insert_one(itinerary.model_dump())
        return str(result.inserted_id) 

    def delete_itinerary(self, itinerary_id: str):
        self.collection.delete_one({"_id": itinerary_id})

    def update_itinerary(self, itinerary_id: str, updated_itinerary: Itinerary):
        self.collection.update_one({"_id": ObjectId(itinerary_id)}, {"$set": updated_itinerary.model_dump()})

    def get_itinerary(self, itinerary_id: str):
        itinerary = self.collection.find_one({"_id": ObjectId(itinerary_id)})

        if itinerary is None:
            raise HTTPException(status_code= 404, detail="Itinerary does not exist")
        
        return itinerary