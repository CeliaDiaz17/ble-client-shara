'''
Uno de los módulos secundarios del sistema. Se encarga de la generacion de preguntas y respuestas del quiz, usando el modulo de OpenAI.
La generación del quiz se guarda en un archivo de texto mientras que las respuestas de SHARA no se almacenan en memoria.
'''

import fitz
import openai
from services.cloud.openai_api import OpenAIAPI

class QuizGenerator:
    
    def __init__(self, open_api: OpenAIAPI):
        self.open_api = open_api
        
    #extraccion texto del pdf proporcionado por el usuario
    def extract_text_pdf(pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    
    def generate_and_save_quiz(self, text, n_questions: int = 5, n_choices: int = 3):
        question_structure = self.open_api.question_structure
        quiz =  self.open_api.generate_quiz(n_questions, n_choices, text)
        answers = self.open_api.generate_answers(quiz, text, question_structure)    
        
        with open("generated_quiz.txt", "w") as file:
            file.write(quiz)
        print("El cuestionario ha sido guardado en 'generated_quiz.txt'")

        with open("quiz_responses.txt", "w") as file:
            file.write(answers)
        print("Las respuestas han sido guardadas en 'quiz_reponses.txt'")
        
        return quiz, answers

