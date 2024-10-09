'''
Module for utility functions.
'''
import json
 
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