'''
Modulo dedicado a la creación de audios a partir del texto y su reproducción. Usa los servicios de Google Text-to-Speech.
'''

from playsound import playsound
from services.cloud.google_api import text_to_speech

class Speaker:
    def __init__(self):
        pass
    
    def read_quiz(self):
        with open("generated_quiz.txt", r) as file:
            quiz = file.read()
        return quiz
    
    def speak(self):
        quiz = self.read_quiz()
        audio = text_to_speech(quiz)
        with open("salida_quiz.wav", "wb") as audio_file:
            audio_file.write(audio)
        return audio

