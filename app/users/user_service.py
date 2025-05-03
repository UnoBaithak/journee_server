from services.db_service import DBService
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from .models.user import User
from auth.utils import AuthUtils

class UserService:
    """Service to handle all user routes and user specific tasks such as profile management"""
    def __init__(self):
        self.collection = DBService().get_collection("users")
    
    def get_user_details(self, username: str):
        user = self.collection.find_one({"username": username})

        if user is None:
            raise HTTPException(404, "User Not found")
        
        return User.from_mongo(user).dao()
    
    def get_user_itineraries(self, username, other_user=False):
        user = self.collection.find_one({"username": username})

        if user is not None:
            return user["itineraries"]
    
        raise  HTTPException(404, "User Not Found")
    
    def update_username(self, userid: str, username: str):
        self.collection.update_one({"_id": userid}, {"$set": {"username": username}})
        response = RedirectResponse(url=f"/user/{username}/itineraries", status_code=302)
        token = AuthUtils.create_token(userid)
        response.set_cookie("b_token", token, httponly=True, secure=False)
        return response
    
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