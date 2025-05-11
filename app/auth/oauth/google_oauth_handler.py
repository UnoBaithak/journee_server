from google.oauth2 import id_token
from google.auth.transport import requests
from auth.models.request_models import GoogleIDResponse
from urllib.parse import parse_qs
import logging

logger = logging.getLogger("uvicorn")

class GoogleOAuthHandler:
    def __init__(self, clientId):
        self.clientId = clientId

    def _validate_client_id(self, request_client_id: str):
        if request_client_id is None:
            raise RuntimeError("ClientId is None")
        
        if request_client_id != self.clientId:
            raise RuntimeError("Invalid Client ID")
        
    def _validate_csrf_token(self, csrf_token):
        pass

    def _process_token(self, credential: str):
        response = id_token.verify_oauth2_token(credential, requests.Request(), self.clientId)
        return GoogleIDResponse(**response)
    
    def process_request_body(self, body: bytes):
        params = parse_qs(body.decode())
        try:
            clientId = params.get('clientId', [None])[0]
            self._validate_client_id(clientId)
            credential = params.get('credential', [None])[0]
            googleId = self._process_token(credential)
            return googleId
        except RuntimeError as e:
            logger.error(f"Failed validation: {e}")
        except ValueError as e:
            logger.error(f"Value error in parsing credentials: {e}")
    
    
