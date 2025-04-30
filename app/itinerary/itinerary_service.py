from services import DBService
from itinerary.models import Itinerary, DayDetails
from bson import ObjectId
from fastapi import HTTPException
import logging

logger = logging.getLogger("uvicorn")

class ItineraryService:

    def __init__(self):
        self.collection = DBService().get_collection("itineraries")

    def create_new_itinerary(self, itinerary: Itinerary):
        logger.info(f"Create a new itinerary for {itinerary.title}")
        result = self.collection.insert_one(itinerary.model_dump())
        return str(result.inserted_id) 

    def delete_itinerary(self, itinerary_id: str):
        logger.info(f"Deleting itinerary {itinerary_id}")
        self.collection.delete_one({"_id": itinerary_id})

    def update_itinerary(self, itinerary_id: str, updated_itinerary: Itinerary):
        logger.info(f"Updating complete itinerary {itinerary_id}")
        self.collection.update_one({"_id": ObjectId(itinerary_id)}, {"$set": updated_itinerary.model_dump()})

    def get_itinerary(self, itinerary_id: str):
        logger.info(f"Get itinerary {itinerary_id} from collection")
        itinerary = self.collection.find_one({"_id": ObjectId(itinerary_id)})

        if itinerary is None:
            logger.error(f"Itinerary with id {itinerary_id} does not exist")
            raise HTTPException(status_code= 404, detail="Itinerary does not exist")
        
        itinerary["_id"] = str(itinerary["_id"])
        
        return itinerary