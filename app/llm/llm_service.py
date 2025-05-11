import os
from dotenv import load_dotenv
from typing import List
from conversations.models import Message

from conversations.services import ConversationService
from llm.llmclient_factory import LLMClientFactory

from common.decorators import Env

import logging
logger = logging.getLogger("uvicorn")

@Env("llm_service.env")
class LLMService:
    def __init__(self):
        self.client = LLMClientFactory.get_llm_client(os.getenv("MODEL_NAME"),
                                                    os.getenv("API_KEY"))
        self.conversation_service = ConversationService()

    def chat(self, conversation_id: str, user_prompt: str):
        logger.info("Fetch history")
        history: List[Message] = self.conversation_service.get_conversation(conversation_id)["messages"]
        logger.info("Chat with the LLM")
        response = self.client.chat(history, user_prompt)
        return response
