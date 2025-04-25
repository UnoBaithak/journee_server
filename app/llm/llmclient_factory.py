from .openai_client_wrapper import OpenAIClient
from .gemini_client_wrapper import GeminiClient

class LLMClientFactory:
    @staticmethod
    def get_llm_client(model: str, api_key: str):
        if model == "OPENAI":
            return "NOT_SUPPORTED"
        elif model == "GEMINI":
            return GeminiClient(api_key)
        else:
            raise RuntimeError("Unsupported LLM model %s", model)
