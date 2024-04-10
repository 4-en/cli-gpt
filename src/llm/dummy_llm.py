import base_llm

class DummyLLM(base_llm.BaseLLM):

    def predict(self, instruction, text):
        return "dummy response: \n[" + text + "]"