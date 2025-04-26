from bson import ObjectId

from .util.message_provider import MessageProvider
from conversations.models import Conversation, Message
from services import DBService
from typing import Literal


class ConversationService:
    def __init__(self):
        self.conversation_collection = DBService().get_collection("conversations")

    def create_conversation(self):

        new_conversation = Conversation()

        result = self.conversation_collection.insert_one(new_conversation.model_dump())
        conversation_id = str(result.inserted_id)

        return conversation_id

    def link_conversation_with_itinerary(self, conversation_id, itinerary_id):
        result = self.conversation_collection.update_one({"_id": ObjectId(conversation_id)}, {"$push": {"itineraries": itinerary_id}})
        if result.modified_count == 0:
            raise RuntimeError("Error in linking conversation to itinerary")

    def update_conversation(self, conversationId: str, message_text: str | dict, role: Literal["user", "assistant"]) -> bool:
        result = self.conversation_collection.update_one({"_id": ObjectId(conversationId)}, {"$push": {"messages": MessageProvider.convert_input_to_message(message_text=message_text, role=role).model_dump()}})
        if result.modified_count == 0:
            return False

        return True

    def get_conversation(self, conversation_id: str):
        return self.conversation_collection.find_one({"_id": ObjectId(conversation_id)})