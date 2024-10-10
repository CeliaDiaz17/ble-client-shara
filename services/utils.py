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
        options_txt += f"Opcion {key}: {value}."
        
    return options_txt

def get_correct(json_data, question_number):
    return json_data[str(question_number)]['correct']

def get_explanation(json_data, question_number):
    return json_data[str(question_number)]['explanation']

#making the prompt for the evaluation feedback
def evaluation_feedback(percentage_correct):
    prompt = f"The following percentage {percentage_correct}  belongs to the percentage of correct answers from different students about a question. Tell me a response in which you mention this percentage and depending on if it's high or low give some adequate feedback to the classroom. In spanish."
    answer = make_request(prompt)
    return answer
    