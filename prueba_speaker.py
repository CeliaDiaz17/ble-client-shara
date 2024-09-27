import time
from services.speaker01 import Speaker
import pyaudio

def main():
    speaker = Speaker()
    p = pyaudio.PyAudio()
    
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=22050, output=True)
    
    for _ in range(5):  # Supongamos que tienes 5 preguntas
        # 1. Reproducir la pregunta
        quiz_audio = speaker.speak_question()
        if quiz_audio:
            stream.write(quiz_audio)
        
        # 2. Esperar el tiempo que los estudiantes tienen para responder
        print("Esperando respuestas de los alumnos...")
        time.sleep(10)  # Pausa de 10 segundos, ajusta según lo necesites
        
        # 3. Reproducir la respuesta correcta
        response_audio = speaker.speak_responses()
        if response_audio:
            stream.write(response_audio)
        
        # 4. Dar feedback sobre la respuesta
        feedback_audio = speaker.speak_feedback()
        if feedback_audio:
            stream.write(feedback_audio)
        
        # 5. Avanzar a la siguiente pregunta
        speaker.next_question()

    # Cerrar el stream
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    main()
