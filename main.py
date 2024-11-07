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

def main():
    quiz = Quiz()
    speaker = Speaker()
    scanner = PassiveBluetoothScanner()
    #ble_manager = BleManager()
    
    #TODO: Sustituir esto por la llamada a la API para que genere un quiz nuevo cada vez    
    json_file_path = "files/quiz.json"
    with open(json_file_path, 'r') as json_file:
        quiz = json.load(json_file)
        
    '''
    async def handle_ble_cycle():
        asyncio.run(pasive_scaning.scan_devices())
        #await ble_manager.ble_cycle() #lanzar escaneo y recoleccion de datos
    '''
    
    #async def scan_responses():
    '''
    print("Scanning for clicker responses...")
    clicker_values = await ble_manager.scan_device()
    print(f"Clicker values collected!: {clicker_values}")
    return clicker_values
    '''
    #asyncio.run(handle_ble_cycle())
    print("INICIO DEL SISTEMA")   
    for question_number in range(1, 5):

        statement = get_statement(quiz, question_number)
        options = get_options(quiz, question_number)
        
        speaker.speak(statement)
        speaker.speak(options)
        time.sleep(5) #tiempo para que los alumnos respondan
        
        device_responses = asyncio.run(scanner.scan_devices())
        #asyncio.run(handle_ble_cycle())
        
        #device_responses = asyncio.run(scan_responses())
        
        #hasta que tengamos la evaluacion
        print(f"Obtained responses: {device_responses}")
        
        correct = get_correct(quiz, question_number)
        explanation = get_explanation(quiz, question_number)
        
        speaker.speak(correct)
        speaker.speak(explanation)
        
        #evaluation and feedback
        correct_answers = get_corrects(quiz, device_responses, question_number)
        total_answ = sum(len(responses) for responses in device_responses)
        #print(f"correct_answ: {correct_answers}")
        #print(f"total answ:{total_answ}")
        percentage_correct = calculate_percent(correct_answers,total_answ)
        
        #print(f"percentage_correct: {percentage_correct}")
        str_feedback = evaluation_feedback(percentage_correct)
        
        speaker.speak(str_feedback)
        
    speaker.speak("Gracias por participar chicos! Hasta la proxima!")
    print("FIN DEL SISTEMA")  


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


