import queue
import json

def get_responses():
    data_queue = queue.Queue()
    
    with open("data.json", "r") as file:
        data = json.load(file)
        print(data)
    
    for item in data:
        data_queue.put(item)
    return data_queue

#redefinir este metodo usando data_queue
def process_responses(responses, correct_answer):
    response_queue = queue.Queue()
    for response in responses:
        response_queue.put(response)
    
    correct_answers = 0
    total_responses = len(responses)

    while not response_queue.empty():
        response = response_queue.get()
        if response == correct_answer:
            correct_answers += 1

    percentage_corrects = (correct_answers / total_responses) * 100
    percentage_incorrects = 100 - percentage_corrects

    return percentage_corrects, percentage_incorrects

def save_results_to_file(filename, results):
    with open(filename, "w") as file:
        for i, (percentage_corrects, percentage_incorrects) in enumerate(results, 1):
            #file.write(f"Ronda {i}:\n")
            file.write(f"Bueno chicos, el: {percentage_corrects:.0f}% de vosotros lo habéis contestado bien, y el {percentage_incorrects:.0f}% lo habéis contestado mal. ¡No os preocupéis! ¡Vamos a por la siguiente ronda!\n\n")    
    print(f"Los resultados han sido guardados en '{filename}'")

# Datos de las respuestas y respuestas correctas
responses_data = [
    (['a', 'b', 'a', 'a', 'a', 'b', 'a', 'c', 'c', 'a'], 'a'),
    (['a', 'b', 'c', 'c', 'c', 'b', 'a', 'c', 'c', 'a'], 'c'),
    (['a', 'b', 'a', 'a', 'b', 'b', 'a', 'c', 'c', 'a'], 'b'),
    (['b', 'b', 'b', 'b', 'a', 'b', 'a', 'b', 'c', 'a'], 'b'),
    (['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'], 'a')
]

results = []

def main ():
    # Procesar todas las respuestas
    for responses, correct_answer in responses_data:
        percentage_corrects, percentage_incorrects = process_responses(responses, correct_answer)
        results.append((percentage_corrects, percentage_incorrects))

    # Guardar todos los resultados en un solo archivo
    save_results_to_file("results.txt", results)
