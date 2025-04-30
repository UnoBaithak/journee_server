from services.db_service import DBService
from fastapi import HTTPException
from .models.user import User

class UserService:
    def __init__(self):
        self.collection = DBService().get_collection("users")
    
    def get_user_details(self, user_id: str):
        user = self.collection.find_one({"_id": user_id})

        if user is None:
            raise HTTPException(404, "User Not found")
        
        return User.from_mongo(user).dao()
    
    def get_user_itineraries(self, user_id, other_user=False):
        user = self.collection.find_one({"_id": user_id})

        if user is not None:
            return user["itineraries"]
    
        raise  HTTPException(404, "User Not Found")
    
    def add_draft_itinerary(self, itinerary_id, conversation_id, user_id):
        self.collection.update_one(
            {"_id": user_id}, 
            {
                "$push": {
                    "itineraries.draft": {
                        "itinerary_id": itinerary_id, 
                        "conversation_id": conversation_id
                    }
                },
                "$setOnInsert": {
                   "itineraries": {
                        "draft": []
                    }
                }
            }, 
            upsert=True)

    def add_conversation(self, conversation_id, user_id):
        self.collection.update_one({"_id": user_id}, {"$push": {"conversations": conversation_id}})