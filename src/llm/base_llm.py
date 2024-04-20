from abc import ABC, abstractmethod
from typing import List
from enum import Enum

class USERS(Enum):
    SYSTEM = 0
    ASSISTANT = 1
    USER = 2


class Message:
    def __init__(self, author: USERS, text: str):
        self.author = author
        self.text = text

class BaseLLM(ABC):

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def predict(self, instruction: str, messages: List[Message]) -> str:
        pass
