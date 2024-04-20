from .base_llm import BaseLLM, Message, USERS
from typing import List

class DummyLLM(BaseLLM):

    def predict(self, instruction: str, messages: List[Message]) -> str:
        return "This is a dummy response"