from services.db_service import DBService
from fastapi import HTTPException
from users.models.user import User
from bson import ObjectId


class UserService:
    """Service to handle all user routes and user specific tasks such as profile management"""

    def __init__(self):
        self.collection = DBService().get_collection("users")

    def get_user_from_id(self, user_id: str):
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        
        if user is None:
            return None
        
        return User.from_mongo(user).username

    def get_user_details(self, username: str):
        user = self.collection.find_one({"username": username})

        if user is None:
            raise HTTPException(404, "User Not found")

        return User.from_mongo(user).dao()

    def get_user_itineraries(self, username, other_user=False):
        user = self.collection.find_one({"username": username})

        if user is not None:
            return user["itineraries"]

        raise HTTPException(404, "User Not Found")
    
    def add_user_itineraries(self, itinerary_id: str, username: str):
        user = self.collection.find_one({"username": username})
        
        if user is not None:
            user["itineraries"]["future"].append(itinerary_id)