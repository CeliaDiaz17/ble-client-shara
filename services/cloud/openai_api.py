import openai
from typing import Dict, Any

class OpenAIAPI:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.default_numquest = 5
        self.default_context = """
        You're an AI assistant with an specialization in creating quizzes for educational purposes based on a PDF provided by the user.
        Your task is to generate a quiz with a given number of questions and answer choices based on the text provided by the user. This questions should be in spanish and follow an specific structure.  
        """
    
    def generate_quiz(self, topic: str, num_questions: int = 5) -> str:
        prompt = f"{self.default_context}"
        

    