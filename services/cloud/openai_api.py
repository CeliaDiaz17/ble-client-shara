import openai
from typing import Dict, Any
import os
import json
import time

class OpenAIAPI:
    def __init__(self, api_key: str, default_numquest=5, num_choices=3, 
                 user_document="/home/celia/Documents/ble-server-shara/files/cicloagua_cortisimo.pdf", 
                 question_structure="Pregunta[Numero que corresponda]: [Pregunta].", cache_dir="cache/"):
        openai.api_key = api_key
        self.default_numquest = default_numquest
        self.num_choices = num_choices
        self.user_document = user_document
        self.question_structure = question_structure
        self.cache_dir = cache_dir
        self.last_request_time = 0 #timecito para limitar las solicitudes y que no pete :')
        self.default_context = """
        You're an AI assistant with an specialization in creating quizzes for educational purposes based on a PDF provided by the user.
        Your task is to generate a quiz with a given number of questions and answer choices based on the text provided by the user. This questions should be in spanish and follow an specific structure.  
        """
        
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    #almacenar resultados en cache
    def cache_result(self, key:str, data:Any):
        cache_path = os.path.join(self.cache_dir, f"{key}.json")
        with open (cache_path, "w") as file:
            json.dump(data, file)
            
    #cargar resultados de cache
    def load_cache(self, key:str):
        cache_path = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(cache_path):
            with open(cache_path, "r") as file:
                return json.load(file)
        return None
    
    #limitar solicitudes
    def rate_limited_request(self, delay: int=2):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < delay:
            time.sleep(delay - time_since_last_request)
        self.last_request_time = time.time()
         
    
    
    '''
    def generate_quiz(self, default_numquest=None, num_choices=None, user_document=None):
        
        numquest = default_numquest if default_numquest else self.default_numquest
        choices = num_choices if num_choices else self.num_choices
        document = user_document if user_document else self.user_document
        
        cache_key = f"quiz_{numquest}_{choices}_{os.path.basename(document)}"
        
        #primero miramos si esta en cache
        cache_result = self.load_cache(cache_key)
        if cache_result:
            print("Loaded from cache")
            return cache_result
        
        self.rate_limited_request()
        
        prompt = f"""{self.default_context}. Generate {self.default_numquest} questions (in spanish) with {self.num_choices} answer choices based on the following text:\n\n{self.user_document}. 
        Every question should start following this structure: {self.question_structure} Mark the correct answer with the symbol '*' next to it corresponding letter.  """
        
        response = openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        #model="gpt-4o-mini",
        model = "gpt-3.5-turbo",
        )
        return response.choices[0].message.content.strip()

    
    def generate_answers(self, quiz, user_document, question_structure):
        
        cache_key = f"answers_{os.path.basename(user_document)}_{quiz[:10]}"  # Usa una parte del quiz para evitar una clave muy larga
        
        #primero miramos si esta en cache
        cache_result = self.load_cache(cache_key)
        if cache_result:
            print("Loaded from cache")
            return cache_result
        
        self.rate_limited_request() 
        
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
            #model="gpt-4o-mini",
            model = "gpt-3.5-turbo",
        )
        
        return response.choices[0].message.content.strip()
        
    '''
    def generate_quiz_with_answers(self):
        
        cache_key = f"quiz_{self.default_numquest}_{self.num_choices}_{os.path.basename(self.user_document)}"
        
        # Busca en el cache primero
        cached_result = self.load_cache(cache_key)
        if cached_result:
            print("Loaded from cache")
            return cached_result

        # Limitar solicitudes por minuto
        self.rate_limited_request()
        
    # Crear el prompt que unifica la generación de preguntas y respuestas
        prompt = f"""
        {self.default_context}. Generate {self.default_numquest} questions (in spanish) with {self.num_choices} answer choices based on the following text:\n\n{self.user_document}. 
        After each question, provide the correct answer with a brief explanation. Every question should follow this structure: {self.question_structure}. 
        Mark the correct answer with the symbol '*' next to the corresponding letter.
        """
        
        # Hacer la solicitud a la API
        response = openai.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",  # Asegúrate de usar el modelo más económico
        )

        full_output = response.choices[0].message.content.strip()

        # Separar las preguntas de las respuestas
        questions_part = []
        answers_part = []

        lines = full_output.split('\n')
        for line in lines:
            if line.startswith("Pregunta"):
                questions_part.append(line)
            elif line.startswith("Respuesta"):
                answers_part.append(line)

        # Guardar las preguntas en el archivo generated_quiz.txt
        with open("generated_quiz.txt", "w") as f:
            f.write("\n".join(questions_part))

        # Guardar las respuestas en el archivo quiz_responses.txt
        with open("quiz_responses.txt", "w") as f:
            f.write("\n".join(answers_part))

        print("Quiz y respuestas guardados en archivos separados.")


    def generate_possible_answ(self, porcentaje_correctas, porcentaje_incorrectas):
        
        cache_key = f"possible_answ_{porcentaje_correctas}_{porcentaje_incorrectas}"
        
        #primero miramos si esta en cache
        cache_result = self.load_cache(cache_key)
        if cache_result:
            print("Loaded from cache")
            return cache_result
        
        self.rate_limited_request() 
        
        prompt = f"""Generate different forms of saying the percentage of correct and incorrect answers which are this values: {porcentaje_correctas} {porcentaje_incorrectas} to encourage 
        the students to keep learning and make them feel good about their progress."""
        
        response = openai.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            #model="gpt-4o-mini",
            model = "gpt-3.5-turbo",

        )
        
        return response.choices[0].message.content.strip()
        
    
        
        

    