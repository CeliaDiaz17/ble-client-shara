'''
Modulo dedicado a la creación de audios a partir del texto y su reproducción. Usa los servicios de Google Text-to-Speech.
'''

import os
import io
from services.cloud.google_api import text_to_speech

class Speaker:
    def __init__(self):
        self.quiz_file = "files/generated_quiz.txt" 
        self.responses_file = "files/quiz_responses.txt"
        self.results_each_quest_file = "files/results.txt"
        self.current_question = 0
        
    def read_quiz_block(self, question_number):
        with open(self.quiz_file, "r") as file:
            lines = file.readlines()
        
        start = None
        end = None
        current_block = 0
        
        for i, line in enumerate(lines):
            if line.startswith(f"Pregunta {question_number + 1}:"):
                start = i
            if line.startswith("Pregunta") and start is not None and current_block > question_number:
                end = i
                break
            if line.startswith("Pregunta"):
                current_block += 1
        
        if start is not None and end is None:
            end = len(lines)
        
        #devuelve el bloque de la pregunta como un solo string
        if start is not None:
            return "".join(lines[start:end]).strip()
        return None
    
    def get_line(self, file, line_number):
        with open(file, "r") as file:
            lines = file.readlines()
        return lines[line_number].strip() if line_number < len(lines) else None  
      
    def speak_question(self):
        question = self.read_quiz_block(self.current_question)
        if question:
            audio = text_to_speech(question)        
            with open("salida_quiz_{self.current_question + 1}.wav", "wb") as audio_file:
                audio_file.write(audio)
            return audio
        return None
    
    def speak_responses(self):
        response = self.get_line(self.responses_file, self.current_question)
        
        if response:
            audio = text_to_speech(response)
            with open("salida_responses_{current_question + 1}.wav", "wb") as audio_file:
                audio_file.write(audio)
            return audio
        return None
    
    def speak_feedback(self):
        results = self.get_line(self.results_each_quest_file, self.current_question)
        
        if results:
            audio = text_to_speech(results)
            with open("salida_results_{current_question + 1}.wav", "wb") as audio_file:
                audio_file.write(audio)
            return audio
        return None
    
    def next_question(self):
        self.current_question += 1
        