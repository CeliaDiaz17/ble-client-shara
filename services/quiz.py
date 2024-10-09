'''
Uno de los módulos secundarios del sistema. Se encarga de la generacion de preguntas y respuestas del quiz, usando el modulo de OpenAI.
La generación del quiz se guarda en un archivo de texto mientras que las respuestas de SHARA no se almacenan en memoria.
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
            Each question should have 3 options, and the correct option should be marked with the symbol * next to it. For each quesiton, provide the correct answer with a brief explanation. 
            The structure for each question should be the following: {self.question_structure}
            Give me that information using the following JSON structure: {self.json_structure}  
        """
        
    def create_quiz(self, quiz_prompt):
        quiz = make_request(quiz_prompt)
        return quiz
    
    
    '''
    def __init__(self, open_api: OpenAIAPI):
        self.open_api = open_api
        self.eval_data = EvaluateData()
        
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
    
    def save_possible_answ(self):
        #si da problema con esta linea probablemente haya que pasarle el porcentaje de correctas e incorrectas. Estan en la clase EvaluateData
        possible_answs = self.open_api.generate_possible_answ()
        
        with open ("possible_answ.txt", "w") as file:
            file.write(possible_answs)
        print("Los resultados han sido guardados en 'possible_answ.txt'")
    '''
