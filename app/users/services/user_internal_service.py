from services.db_service import DBService
from bson import ObjectId


class UserInternalService:
    """Service to handle all user routes and user specific tasks such as profile management"""

    def __init__(self):
        self.collection = DBService().get_collection("users")

    def add_draft_itinerary(self, itinerary_id, user_id):
        self.collection.update_one(
            {"_id": user_id},
            {
                "$push": {
                    "itineraries.draft": itinerary_id
                },
                "$setOnInsert": {"itineraries": {"draft": []}},
            },
            upsert=True,
        )

    def add_conversation(self, conversation_id, user_id):
        self.collection.update_one(
            {"_id": user_id}, {"$push": {"conversations": conversation_id}}
        )

    def can_user_edit_itinerary(self, user_id: str, itinerary_id: str):
        document = self.collection.find_one({"_id": ObjectId(user_id)}, {"itineraries": 1})
        if document is None:
            return False
        
        itineraries = document.get("itineraries", None)
        if itineraries is None:
            return False 
        for _, itineraryList in itineraries.items():
            if itinerary_id in itineraryList:
                return True
        
        return False
    
    def get_related_conversation(self, user_id: str, itineraryId: str) -> str | None:
        document = self.collection.find_one({"_id": ObjectId(user_id)}, {"conversations": 1})
        if document is None:
            return None
        
        conversations = document.get("conversations", None)
        if conversations is None:
            return None
        
        for conversation in conversations:
            if conversation["itinerary_id"] == itineraryId:
                return conversation["conversation_id"]
        
        return None
