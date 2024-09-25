'''
Módulo principal del programa. Este se ejecutará en el SHARA (cliente) y se encargara de 
coordinar la conectividad con los dispositivos BLE, y usará el resto de módulos del programa 
para generar y evaluar preguntas, y reproducir los resultados. 
'''
import sys
import os
import asyncio
import random
import playsound
from ble_client_shara import BleManager
from services.logic_gen_quiz import QuizGenerator
from services.cloud.openai_api import OpenAIAPI
from services.speaker01 import Speaker
from services.evaluacion_datos import EvaluateData


class Main:
    def __init__(self, api_key: str):
        api_key = os.getenv("OPENAI_API_KEY")
        self.openai_api = OpenAIAPI(api_key)
        self.gen_quiz = QuizGenerator(self.openai_api)
        self.ble_client_shara = BleManager()
        self.speaker = Speaker()
        self.eval_data = EvaluateData()

    async def run(self):
        user_document = self.openai_api.user_document
        end_loop = self.ble_client_shara.MAX_RECONNECT
        loop_iter = 0
        
        with open("generated_quiz.txt", "r") as file:
            quiz = file.readlines()
        
        #Llamadas para generacion del quiz y respuestas
        self.gen_quiz.generate_and_save_quiz(user_document, num_questions=5, num_choices=3)

        #Establecer conexion BLE
        await self.ble_client_shara.ble_cycle() #asegurar que esto ocurre a la vez que todo lo demas
        
        #Mientras el numero de preguntas sea menor a 5
        while loop_iter < end_loop:
            #Reproducir pregunta (matizar que reproduzca solo la que toque en cada iteracion)
            pregunta = self.get_pregunta(self.loop_iter, quiz)
            audio_pregunta = self.speaker.speak(pregunta)
            playsound(audio_pregunta)
            #Recibir respuesta (no se si deberia ir el speaker en el await tambien)
            await asyncio.gather(self.ble_client_shara.ble_cycle())
            #Evaluar respuesta
            respuestas_dispositivos = self.ble_client_shara.current_round_data
            respuestas_correctas = self.eval_data.leer_respuestas_correctas("correct_answers.json")
            self.eval_data.evaluar(respuestas_dispositivos, respuestas_correctas)
            #Reproducir feedback de la respuesta
            with open("quiz_responses.txt", "r") as file:
                all_lines = file.readlines()
                random_line = random.choice(all_lines)
            feedback = self.speaker.speak(random_line)
            playsound(feedback)
            #Cierre, explicacion final
            with open("resultados_generales.txt", "r") as file:
                general_results = file.read()
            final_feedback = self.speaker.speak(general_results)
            playsound(final_feedback)
            loop_iter += 1 
        goodbye = self.speaker.speak("¡Un placer haber jugado con vosotros! ¡Chaito!")
        playsound(goodbye)
    
    def get_pregunta(self, iteracion, preguntas):
        start_idx = iteracion * 4
        return "".join(preguntas[start_idx:start_idx + 4])
#Ciere conexion BLE
