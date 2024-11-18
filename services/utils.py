'''
Module for utility functions.
'''

import json
from services.cloud.openai_api import make_request
 
#get specific json parts
def get_statement(json_data, question_number):
    return json_data[str(question_number)]['statement']

def get_options(json_data, question_number):
    options = json_data[str(question_number)]['options']
    
    options_txt = ""
    for key, value in options.items():
        options_txt += f"Opción {key}: {value}."
        
    return options_txt

def get_correct(json_data, question_number):
    return json_data[str(question_number)]['correct']

def get_explanation(json_data, question_number):
    return json_data[str(question_number)]['explanation']

#making gpt prompt for the evaluation feedback
def evaluation_feedback(percentage_correct):
    prompt = f"Con base en que el {percentage_correct}% de los estudiantes respondió correctamente la última pregunta, genera una frase breve y motivadora para la clase, destacando lo que pueden mejorar o felicitándolos si el porcentaje es alto. En español."
    answer = make_request(prompt)
    return answer
    