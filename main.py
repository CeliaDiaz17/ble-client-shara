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
from ble_client import BleManager
from services.data_evaluation import  get_corrects, calculate_percent

def main():
    quiz = Quiz()
    speaker = Speaker()
    ble_manager = BleManager()
    
    
    json_file_path = "files/quiz.json"
    with open(json_file_path, 'r') as json_file:
        quiz = json.load(json_file)
        
    async def handle_ble_cycle():
        await ble_manager.ble_cycle()


    for question_number in range(1, 5):

        statement = get_statement(quiz, question_number)
        options = get_options(quiz, question_number)
        
        speaker.speak(statement)
        speaker.speak(options)
        time.sleep(5) #tiempo para que los alumnos respondan
        
        asyncio.run(handle_ble_cycle())
        
        responses = ble_manager.current_round_data
        
        #hasta que tengamos la evaluacion
        print(f"Respuestas obtenidas: {responses}")
        
        correct = get_correct(quiz, question_number)
        explanation = get_explanation(quiz, question_number)
        
        speaker.speak(correct)
        speaker.speak(explanation)
        
        #evaluation and feedback
        correct_answers = get_corrects(quiz, responses, question_number)
        total_answ = len(responses)
        percentage_correct = calculate_percent(correct_answers,total_answ)
        str_feedback = evaluation_feedback(percentage_correct)
        
        speaker.speak(str_feedback)
        


if __name__ == "__main__":
    main()



#CODIGO AUXILIAR

    '''
    MICKY HERRAMIENTA QUE USAREMOS MAS TARDE
    
    json_file_path = "files/quiz.json"
    
    str_quiz = quiz.create_quiz(quiz.quiz_prompt)
    
    dict_quiz = json.loads(str_quiz)
        
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(dict_quiz, json_file, ensure_ascii=False, indent=4)
    '''


