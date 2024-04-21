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
    def __init__(self, author: USERS, text: str, timestamp=None):
        self.timestamp = timestamp or int(time.time())
        self.author = author
        self.text = text

    def to_json_dict(self):
        return {
            "timestamp": self.timestamp,
            "author": self.author.name,
            "text": self.text
        }
    
    @staticmethod
    def from_json_dict(data):
        author = USERS[data["author"]]
        text = data["text"]
        m = Message(author, text, data["timestamp"])
        return m

class BaseLLM(ABC):

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def predict(self, instruction: str, messages: List[Message]) -> str:
        pass
