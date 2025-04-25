from typing import Literal
from conversations.models.message import Message


class MessageProvider:
    def __init__(self):
        pass

    @staticmethod
    def convert_input_to_message(message_text: str | dict, role: Literal["user", "assistant", "system"]):
        """Converts user input to a message object"""
        message = Message() \
                    .with_role(role) \
                    .with_message(message_text)

        return message
        