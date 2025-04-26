from .db_service import DBService

class UserMetadataService:
    
    def __init__(self):
        self.collection = DBService().get_collection("user_metadata")

    def add_draft_itinerary(self, itinerary_id, user_id):
        self.collection.update_one({"user_id": user_id}, {"$push": {"itineraries.draft": itinerary_id}}, upsert=True)

    def add_conversation(self, conversation_id, user_id):
        self.collection.update_one({"user_id": user_id}, {"$push": {"conversations": conversation_id}})