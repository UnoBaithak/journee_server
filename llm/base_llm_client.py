from abc import ABC, abstractmethod
class BaseClient(ABC):
    def __init__(self, stream: bool):
        self.stream = stream

    @abstractmethod
    def generate_text(self, user_input: str) -> str:
        pass