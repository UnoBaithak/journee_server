from enum import Enum
from common.decorators import Env
from .oauth.google_oauth_handler import GoogleOAuthHandler
from services import DBService
import os
import logging

logger = logging.getLogger("uvicorn")

class OAuthProvider(str, Enum):
    GOOGLE = "google"

@Env("auth_service.env")
class OAuthHandler:
    def __init__(self):
        self.google_oauth_handler = GoogleOAuthHandler(os.getenv("GOOGLE_CLIENT_ID"))
        self.user_collection = DBService().get_collection("users")

    def process_request_body(self, request_body: bytes, oauth_provider: OAuthProvider):
        if oauth_provider == OAuthProvider.GOOGLE:
            logger.info("Google oauth handler handling the body")
            processed_details = self.google_oauth_handler.process_request_body(request_body)
            if processed_details is None:
                raise RuntimeError("asdsad")
            
            return processed_details
            
            