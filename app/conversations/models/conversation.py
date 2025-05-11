from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from .message import Message


class Conversation(BaseModel):
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)