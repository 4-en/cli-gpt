import openai
import base_llm

class GPT3(base_llm.BaseLLM):
    def __init__(self, api_key, model="davinci"):
        openai.api_key = api_key
        self.model = model

    def predict(self, instruction, text):
        response = openai.Completion.create(
            engine=self.model,
            prompt=instruction + text,
            max_tokens=100
        )
        return response.choices[0].text
    

class GPT4(base_llm.BaseLLM):
    def __init__(self, api_key, model="davinci"):
        openai.api_key = api_key
        self.model = model

    def predict(self, instruction, text):
        response = openai.Completion.create(
            engine=self.model,
            prompt=instruction + text,
            max_tokens=100
        )
        return response.choices[0].text