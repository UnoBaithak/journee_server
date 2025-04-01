from .base_llm_client import BaseClient
from google import genai
from models.data_models import Itinerary

class GeminiClient(BaseClient):
    def __init__(self, api_key, stream = False):
        super().__init__(stream)
        self.client = genai.Client(api_key=api_key)
    
    def generate_text(self, user_input: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_input,
            config = {
                'response_mime_type': 'application/json',
                'response_schema': Itinerary
            }
        )
        return response.parsed