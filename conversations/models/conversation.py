from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from .message import Message


class Conversation(BaseModel):
    # conversation id is the unique mongo db id
    messages: List[Message] = []
    itinerary_id: Optional[str] = Field(description="Itinerary id for which this conversation is based", default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def with_itinerary_id(self, itinerary_id):
        self.itinerary_id = itinerary_id
        return self

    def with_messages(self, messages):
        self.messages = messages
        return self