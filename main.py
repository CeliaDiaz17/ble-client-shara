'''
Módulo principal del programa. Este se ejecutará en el SHARA (cliente) y se encargara de 
coordinar la conectividad con los dispositivos BLE, y usará el resto de módulos del programa 
para generar y evaluar preguntas, y reproducir los resultados. 
'''
import sys
import os
from ble_client_shara import BleManager
from services.logic_gen_quiz import QuizGenerator
from services.cloud.openai_api import OpenAIAPI

class Main:
    def __init__(self, api_key: str):
        api_key = os.getenv("OPENAI_API_KEY")
        self.openai_api = OpenAIAPI(api_key)
        self.gen_quiz = QuizGenerator(self.openai_api)
        self.ble_client_shara = BleManager()

    async def run(self):
        user_document = self.openai_api.user_document
        end_loop = self.ble_client_shara.MAX_RECONNECT
        loop_iter = 0
        
        #Llamadas para generacion del quiz y respuestas
        quiz, answers = self.gen_quiz.generate_and_save_quiz(user_document, num_questions=5, num_choices=3)

        #Establecer conexion BLE
        await self.ble_client_shara.ble_cycle() #asegurar que esto ocurre a la vez que todo lo demas
        
        #Mientras el numero de preguntas sea menor a 5
        while loop_iter < end_loop:
            #Reproducir pregunta
            #Recibir respuesta
            #Evaluar respuesta
            #Reproducir feedback de la respuesta
            #Cierre, explicacion final
            loop_iter += 1 








#Ciere conexion BLE
