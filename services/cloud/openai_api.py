import openai
from typing import Dict, Any

class OpenAIAPI:
    def __init__(self, api_key: str, default_numquest=5, num_choices=3, 
                 user_document="/home/celia/Documents/ble-server-shara/files/tema_vertebrados_ESO.pdf", 
                 question_structure="Pregunta[Numero que corresponda]: [Pregunta]."):
        openai.api_key = api_key
        self.default_numquest = default_numquest
        self.num_choices = num_choices
        self.user_document = user_document
        self.question_structure = question_structure
        self.default_context = """
        You're an AI assistant with an specialization in creating quizzes for educational purposes based on a PDF provided by the user.
        Your task is to generate a quiz with a given number of questions and answer choices based on the text provided by the user. This questions should be in spanish and follow an specific structure.  
        """
    
    def generate_quiz(self, default_numquest=None, num_choices=None, user_document=None):
        
        numquest = default_numquest if default_numquest else self.default_numquest
        choices = num_choices if num_choices else self.num_choices
        document = user_document if user_document else self.user_document
        
        prompt = f"""{self.default_context}. Generate {self.default_numquest} questions (in spanish) with {self.num_choices} answer choices based on the following text:\n\n{self.user_document}. 
        Every question should start following this structure: {self.question_structure} Mark the correct answer with the symbol '*' next to it corresponding letter.  """
        
        response = openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4",
        )
        return response.choices[0].message.content.strip()

    
    def generate_answers(self, quiz, user_document, question_structure):
        prompt = f"""Given the following quiz, answer every question with the correct choice (a, b, c). Then provide a brief explanation about why it is correct, base this explanation on this text:\n\n{user_document}. 
        Use the structure: \n\n{question_structure}. The quiz is as follows:\n\n{quiz}. Just follow the structure provided for all the answers."""

        response = openai.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "temperature": 0.1,
                }
            ],
            model="gpt-4",
        )
        
        return response.choices[0].message.content.strip()

    def generate_possible_answ(self, porcentaje_correctas, porcentaje_incorrectas):
        prompt = f"""Generate different forms of saying the percentage of correct and incorrect answers which are this values: {porcentaje_correctas} {porcentaje_incorrectas} to encourage 
        the students to keep learning and make them feel good about their progress."""
        
        response = openai.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4",

        )
        
        return response.choices[0].message.content.strip()
        
    
        
        

    