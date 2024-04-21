import openai
from .base_llm import BaseLLM, Message, USERS, APIKeyError
from typing import List

class GPT(BaseLLM):
    def __init__(self, api_key=None, model="None", *args, **kwargs):
        super().__init__(*args, **kwargs)
        if api_key is None or api_key == "None":
            raise APIKeyError("API Key is required for OpenAI Models")
        if model == "None":
            raise ValueError("Model is required for OpenAI Models")
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def predict(self, instruction, text):
        return self._generate_response(instruction, text)
    
    def _user_to_openai(self, user: USERS) -> str:
        if user == USERS.SYSTEM:
            return "system"
        elif user == USERS.ASSISTANT:
            return "assistant"
        elif user == USERS.USER:
            return "user"
        else:
            return "user"

    def _generate_response(self, instruction: str, messages: List[Message]) -> str | None:
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": instruction},
                    *[
                        {
                            "role": self._user_to_openai(message.author),
                            "content": message.text
                        } for message in messages
                    ]
                ],
                max_tokens=256,
                temperature=0.8,
                response_format = {"type": "json_object"}
            )
            if completion.choices[0].message.content.startswith("<Herobrine> "):
                return completion.choices[0].message.content[12:]
            return completion.choices[0].message.content
        except Exception as e:
            print("Failed to generate text")
            print(e)
            return None

class GPT3(GPT):
    def __init__(self, api_key=None, model="gpt-3.5-turbo", *args, **kwargs):
        super().__init__(api_key, model, *args, **kwargs)
    

class GPT4(GPT3):
    def __init__(self, api_key=None, model="gpt-4-turbo"):
        super().__init__(api_key, model)
    