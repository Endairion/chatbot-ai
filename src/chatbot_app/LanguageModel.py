import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class LanguageModel:
    def __init__(self, model_name: str, temperature: float):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = model_name
        self.temperature = temperature
        self.model = None

    def __enter__(self):
        if self.model is None:
            self.model = ChatOpenAI(model=self.model_name, temperature=self.temperature, api_key=self.api_key)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # If there is any cleanup needed, it should be done here
        self.model = None

    def generate(self, prompt: str) -> str:
        response = self.model.invoke(prompt)
        response_text = response.content
        return response_text