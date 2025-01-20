import json
import logging
import time
import asyncio
import threading
from datetime import datetime
import os
from services.quiz import Quiz
from services.speaker import Speaker
from services.utils import get_correct, get_explanation, get_options, get_statement, evaluation_feedback
from pasive_scaning import PassiveBluetoothScanner
from services.data_evaluation import  get_corrects, calculate_percent
import cv2 as cv
from SHARA.services.eyes.service import Eyes
from evdev import InputDevice, categorize, ecodes

running = True
TOUCH_DEVICE_PATH = "/dev/input/event4"

class SystemPausedException(Exception):
    pass

resume_event = threading.Event()
resume_event.set()
lock=threading.Lock()


def touch_listener():
    dev = InputDevice(TOUCH_DEVICE_PATH)
    print(f"Escuchando eventos en: {dev.name}")
    
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY and event.code == ecodes.BTN_TOUCH:
            if event.value == 1:
                resume_event.set()
    
def setup_logging(log_directory='logs'):
    # Crear el directorio de logs si no existe
    os.makedirs(log_directory, exist_ok=True)
    
    # Crear un nombre de archivo único con la fecha actual
    log_filename = f"system_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Construir la ruta completa del archivo de log
    full_log_path = os.path.join(log_directory, log_filename)
    
    # Configurar el logging
    logging.basicConfig(
        filename=full_log_path, 
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    return full_log_path 

    

async def quiz_logic(eyes):
    quiz = Quiz()
    speaker = Speaker()
    scanner = PassiveBluetoothScanner()
    
    #TODO: Sustituir esto por la llamada a la API para que genere un quiz nuevo cada vez    
    
    
    json_file_path = "files/quiz.json"
    with open(json_file_path, 'r') as json_file:
        json_quiz = json.load(json_file)
    
    
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
        json_quiz = json.load(json_file)
    '''   
      
    
    connected_devices = await scanner.handshake()
    num_devices = len(connected_devices)
    
    logging.info("INICIO DEL SISTEMA")   
    speaker.speak(f"Sistema preparado. {num_devices} dispositivos conectados. Toque la pantalla para comenzar.")
    resume_event.clear()
    resume_event.wait()
    speaker.speak("Bienvenidos a todos y a todas! Vamos a comenzar un cuestionario de 3 preguntas sobre el temario. Estad atentos. Tendréis 15 segundos para contestar cada pregunta. ¡Suerte!")
    for question_number in range(1, 4):
        
        statement = get_statement(json_quiz, question_number)
        options = get_options(json_quiz, question_number)
        
        eyes.set('neutral')
        speaker.speak(statement)
        speaker.speak(options)
        speaker.speak("Desde ahora, teneis 15 segundos para responder")
        
        time.sleep(15)
            
        device_responses = await scanner.retrieve_device_data()
                        
        logging.info(f"Obtained responses: {device_responses}")
        
        correct = get_correct(json_quiz, question_number)
        explanation = get_explanation(json_quiz, question_number) 
        
        speaker.speak("La opción correcta es la")
        speaker.speak(correct)
        speaker.speak(explanation)
        
        #evaluation and feedback
        correct_answers = get_corrects(json_quiz, device_responses, question_number)
        total_answ = sum(len(responses) for responses in device_responses)
        
        percentage_correct = calculate_percent(correct_answers,total_answ)
        if percentage_correct > 60.0:
            eyes.set('joy')
        elif percentage_correct < 40.0:
            eyes.set('sad')
        
        
        str_feedback = evaluation_feedback(percentage_correct) 
        
        speaker.speak(str_feedback)
        #speaker.speak("Aqui te estoy dando un feedback guapísimo y ahora deberia pararme")
        

        logging.info("Sistema pausado automaticamente")
        speaker.speak("Sistema pausado, para continuar toque la pantalla")
        logging.info("Esperando que se toque la pantalla para continuar")
        resume_event.clear()
        resume_event.wait()
        speaker.speak("¡Genial! Continuamos")
        
    eyes.set('joy')
    speaker.speak("Gracias por participar chicos! Hasta la proxima!")
    logging.info("FIN DEL SISTEMA") 


async def main():
    log_file = setup_logging()
    eyes = Eyes(faces_dir='../faces_brown', face_cache='../faces_cache_brown', sc_width=600, sc_height=1024)
    threading.Thread(target=touch_listener, daemon=True).start()
    await quiz_logic(eyes)
            
            
            
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt: 
        eyes.stop()
        
        #hola


