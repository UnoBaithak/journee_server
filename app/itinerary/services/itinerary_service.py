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
        itinerary.metadata.clonedFrom = None
        for (idx, dayDetails) in enumerate(itinerary.details):
            dayDetails.day_id = idx+1
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
    
    def clone_itinerary(self, original_itinerary_id: str, user_id: str):
        itinerary = self.collection.find_one({"_id": ObjectId(original_itinerary_id)})
        del itinerary["_id"]
        new_itinerary = Itinerary(**itinerary)
        new_itinerary.metadata.clonedFrom = original_itinerary_id
        new_itinerary.metadata.creatorId = user_id
        new_itinerary_id = self.collection.insert_one(new_itinerary.model_dump())
        return new_itinerary_id