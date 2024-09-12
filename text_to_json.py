import json
import re

def text_to_json(generated_quiz_filepath, json_filepath):
    data = []

    with open(generated_quiz_filepath, "r") as file:
        question_number = None
        correct_answer = None
        
        for line in file:
            line = line.strip()
            if line.startswith("Pregunta"):
                if question_number and correct_answer:
                    data.append({
                        "question": question_number,
                        "correct_answer": correct_answer
                    })
                    correct_answer = None
                    
                # Extraer solo el número de la pregunta usando una expresión regular
                match = re.search(r"Pregunta\s+(\d+):", line)
                if match:
                    question_number = match.group(1)
            elif line.endswith("*"):
                    correct_answer = line[0]
        
        if question_number and correct_answer:
            data.append({
                "question": question_number,
                "correct_answer": correct_answer,
            })
                
    with open(json_filepath, "w") as json_file:
        json.dump(data, json_file, indent=4)
        
text_to_json("generated_quiz.txt", "correct_answers.json")
                    