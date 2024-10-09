import openai
from typing import Dict, Any
import os

   
api_key = os.getenv("OPENAI_API_KEY")
    
def make_request(prompt):
    response = openai.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",  # Asegúrate de usar el modelo mas economico
)     
    full_output = response.choices[0].message.content.strip()
    return full_output
    
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
'''      
    
        
        

    