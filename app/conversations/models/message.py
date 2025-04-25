from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Literal, Union

class Message(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid4()))
    role: Literal["user", "assistant", "system"] = Field("Whose message is this")
    message: Union[str, dict] = Field("", description="The message string or a dictionary like an itinerary")

    def with_role(self, role: str):
        return self.model_copy(update={"role": role})

    def with_message(self, message: Union[str, dict]):
        return self.model_copy(update={"message": message})