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
from services.utils import get_correct, get_explanation, get_options, get_statement
from ble_client import BleManager

def main():
    quiz = Quiz()
    speaker = Speaker()
    ble_manager = BleManager()
    
    #speaker.speak("hola")
    
    
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



'''
def main():
    print("INICIO DE SISTEMA")
    user_document = self.openai_api.user_document
    end_loop = self.ble_client_shara.MAX_RECONNECT
    loop_iter = 0
    stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=22050, output=True)
        
    #Llamada para generacion del quiz y respuestas

    #Mientras el numero de preguntas sea menor a 5
    for question_number in range(0, end_loop):
            
        #Reproducir pregunta 
        print(f"Reproduciendo pregunta: {question_number}...")
        quiz_audio = self.speaker.speak_question(question_number)
        if quiz_audio:
            stream.write(quiz_audio)           
            
        #Recibe respuesta que esta en current_round_data
            
        #Evaluar respuesta
        respuestas_dispositivos = self.ble_client_shara.current_round_data
        respuestas_correctas = self.eval_data.leer_respuestas_correctas("files/correct_answers.json")
        self.eval_data.evaluar_respuestas(respuestas_dispositivos, respuestas_correctas)
            
        #Reproducir feedback de la respuesta
        print(f"Reproduciendo respuesta: {question_number}...")
        response_audio = self.speaker.speak_responses(question_number)
        if response_audio:
            stream.write(response_audio)
        print(f"Reproduciendo feedback respuesta: {question_number}...")
        feedback_audio = self.speaker.speak_feedback(question_number)
        if feedback_audio:
            stream.write(feedback_audio)
            
            #Avanzar a la siguiente pregunta
            #loop_iter += 1
            #self.speaker.next_question()
            
    #Cierre, explicacion final 
    with open("files/resultados_generales.txt", "r") as file:
        general_results = file.read()
    final_feedback = self.speaker.speak(general_results)
    stream.write(final_feedback)
        
        #Despedida en alto 
           
    goodbye = self.speaker.speak("¡Un placer haber jugado con vosotros! ¡Chaito!")
    stream.write(goodbye)
                
    self.stream.stop_stream()
    self.stream.close()
    self.p.terminate()
    print("FIN DE SISTEMA")
        
def get_pregunta(self, iteracion, preguntas):
    start_idx = iteracion * 4
    return "".join(preguntas[start_idx:start_idx + 4])
'''

