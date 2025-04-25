from .base_llm_client import BaseClient
from openai import OpenAI

class OpenAIClient(BaseClient):
    def __init__(self, api_key, stream=False):
        super().__init__(stream)
        self.client = OpenAI(api_key=api_key)
    
    def generate_text(self, user_input):
        return None