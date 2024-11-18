'''
Has everything regarding the quiz. Also have the method for creating the quiz.
'''

from services.cloud.openai_api import make_request


class Quiz:
    def __init__(self):
        self.user_document = "/home/celia/Documents/ble-server-shara/files/cicloagua_corto.pdf"
        self.question_structure = "Pregunta[Numero que corresponda]:[Pregunta]"
        self.json_structure = """{{
    "1": {{
        "statement": "Question statement 1",
        "options": {{
            "a": "option a",
            "b": "option b",
            "c": "option c"
        }},
        "correct": "a",
        "explanation": "Explanation of why option a is correct"
    }},
    "2": {{
        "statement": "Question statement 2",
        "options": {{
            "a": "option a",
            "b": "option b",
            "c": "option c"
        }},
        "correct": "b",
        "explanation": "Explanation of why option b is correct"
    }}
    // Continue with more questions in the same format
}}"""
        self.quiz_prompt = f"""
            Given the following content from the PDF {self.user_document}, generate a quiz in Spanish with 5 questions.
            Each question should have 3 options. For each quesiton, provide the correct answer with a brief explanation. Don't be too verbose, but be friendly, you are interacting with 10 year old kids. 
            The structure for each question should be the following: {self.question_structure}
            Give me that information using the following JSON structure(without any additional text or explanation outside the JSON): {self.json_structure}  
        """
        
    def create_quiz(self, quiz_prompt):
        quiz = make_request(quiz_prompt)
        return quiz
    
    
    