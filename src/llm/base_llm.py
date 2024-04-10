from abc import ABC, abstractmethod


class BaseLLM(ABC):

    @abstractmethod
    def predict(self, instruction, text):
        pass
