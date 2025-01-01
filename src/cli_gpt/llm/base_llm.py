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
    def __init__(self, author: USERS, text: str, timestamp=None, summary=None):
        self.timestamp = timestamp or int(time.time())
        self.author = author
        self.text = text
        self.summary = summary or None

    def to_json_dict(self):
        return {
            "timestamp": self.timestamp,
            "author": self.author.name,
            "text": self.text,
            "summary": self.summary,
        }
    
    @staticmethod
    def from_json_dict(data):
        author = USERS[data.get("author", "USER")]
        text = data.get("text", "")
        summary = data.get("summary", None)
        timestamp = data.get("timestamp", int(time.time()))
        return Message(author, text, timestamp, summary)
    
    def __str__(self):
        return f"{self.author.name} ({self.timestamp}): {self.text}"
    
    def __repr__(self):
        return self.__str__()

class BaseLLM(ABC):

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def predict(self, instruction: str, messages: List[Message]) -> str:
        pass
