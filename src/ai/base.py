from abc import ABC, abstractmethod

class AIPlatform(ABC):
    @abstractmethod
    def chat(self, prompt: str) -> str:
        """Sends prompt to AI and return response text"""
        pass