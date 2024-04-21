from abc import ABC, abstractmethod
from typing import List
from enum import Enum
import time

class APIKeyError(Exception):
    def __init__(self, message="API key not set."):
        self.message = message
        super().__init__(self.message)

class USERS(Enum):
    SYSTEM = 0
    ASSISTANT = 1
    USER = 2


class Message:
    def __init__(self, author: USERS, text: str):
        self.timestamp = int(time.time())
        self.author = author
        self.text = text

class BaseLLM(ABC):

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def predict(self, instruction: str, messages: List[Message]) -> str:
        pass
