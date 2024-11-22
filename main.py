'''
Módulo principal del programa. Este se ejecutará en el SHARA (cliente) y se encargara de 
coordinar la conectividad con los dispositivos BLE, y usará el resto de módulos del programa 
para generar y evaluar preguntas, y reproducir los resultados. 
'''

import json
import time
import asyncio
from services.quiz import Quiz
from services.speaker import Speaker
from services.utils import get_correct, get_explanation, get_options, get_statement, evaluation_feedback
from pasive_scaning import PassiveBluetoothScanner
from services.data_evaluation import  get_corrects, calculate_percent

#TODO: Implementar el pasive_scaning en el main

async def main():
    quiz = Quiz()
    speaker = Speaker()
    scanner = PassiveBluetoothScanner()

    await scanner.handshake()
    
    #TODO: Sustituir esto por la llamada a la API para que genere un quiz nuevo cada vez    
    
    json_file_path = "files/quiz.json"
    with open(json_file_path, 'r') as json_file:
        quiz = json.load(json_file)
    
    '''
    json_file_path = "files/quiz.json"
    
    str_quiz = quiz.create_quiz(quiz.quiz_prompt)
    print(str_quiz)
    
    # Verificar si str_quiz es válido antes de convertirlo
    if str_quiz and str_quiz.strip().startswith('{'):
        try:
            dict_quiz = json.loads(str_quiz)
            print("JSON cargado correctamente")
            # Guardar el JSON en un archivo
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(dict_quiz, json_file, ensure_ascii=False, indent=4)
        except json.JSONDecodeError as e:
            print("Error al cargar el JSON:", e)
    else:
        print("Error: `str_quiz` no contiene un JSON válido.")
    
    with open(json_file_path, 'r') as json_file:
        quiz = json.load(json_file)
    '''    

    print("INICIO DEL SISTEMA")   
    speaker.speak("Bienvenidos a todos y a todas! Vamos a comenzar un cuestionario de 4 preguntas sobre el temario. Estad atentos. Tendréis 15 segundos para contestar cada pregunta. ¡Suerte!")
    for question_number in range(1, 5):

        statement = get_statement(quiz, question_number)
        options = get_options(quiz, question_number)
        
        speaker.speak(statement)
        speaker.speak(options)
        speaker.speak("Desde ahora, teneis 15 segundos para responder")
        time.sleep(15) #tiempo para que los alumnos respondan
        
        device_responses = await scanner.retrieve_device_data()
        
        print(f"Obtained responses: {device_responses}")
        
        correct = get_correct(quiz, question_number)
        explanation = get_explanation(quiz, question_number)
        
        speaker.speak(correct)
        speaker.speak(explanation)
        
        #evaluation and feedback
        correct_answers = get_corrects(quiz, device_responses, question_number)
        total_answ = sum(len(responses) for responses in device_responses)
        percentage_correct = calculate_percent(correct_answers,total_answ)
        
        str_feedback = evaluation_feedback(percentage_correct)
        
        speaker.speak(str_feedback)
        
    speaker.speak("Gracias por participar chicos! Hasta la proxima!")
    print("FIN DEL SISTEMA")  


loop = asyncio.get_event_loop()
loop.run_until_complete(main())



#CODIGO AUXILIAR

'''
MICKY HERRAMIENTA QUE USAREMOS MAS TARDE

json_file_path = "files/quiz.json"

str_quiz = quiz.create_quiz(quiz.quiz_prompt)

dict_quiz = json.loads(str_quiz)
    
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(dict_quiz, json_file, ensure_ascii=False, indent=4)
'''


