import queue

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

# Procesar todas las respuestas
for responses, correct_answer in responses_data:
    percentage_corrects, percentage_incorrects = process_responses(responses, correct_answer)
    results.append((percentage_corrects, percentage_incorrects))

# Guardar todos los resultados en un solo archivo
save_results_to_file("results.txt", results)
























'''
response_queue_first = queue.Queue()
response_queue_scnd = queue.Queue()
response_queue_thrd = queue.Queue()
response_queue_fourth = queue.Queue()
response_queue_fifth = queue.Queue()



responses_first = ['a', 'b', 'a', 'a', 'a', 'b', 'a', 'c', 'c', 'a']
correct_answer_first = 'a'

responses_scnd = ['a', 'b', 'c', 'c', 'c', 'b', 'a', 'c', 'c', 'a']
correct_answer_scnd = 'c'

responses_thrd = ['a', 'b', 'a', 'a', 'b', 'b', 'a', 'c', 'c', 'a']
correct_answer_thrd = 'b'

responses_frth = ['b', 'b', 'b', 'b', 'a', 'b', 'a', 'b', 'c', 'a']
correct_answer_frth = 'b'

responses_fifth = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']
correct_answer_fifth = 'a'

for response in responses_first:
    response_queue_first.put(response)
    
correct_answers_first = 0
total_responses_first = len(responses_first)

while not response_queue_first.empty():
    response = response_queue_first.get()
    if response == correct_answer_first:
        correct_answers_first += 1
        
percentage_corrects_first = (correct_answers_first / total_responses_first) * 100
percentage_incorrects_first = 100 - percentage_corrects_first

with open("results.txt", "w") as file:
    file.write(f"Bueno chicos, el: {percentage_corrects_first:.2f}% de vosotros lo habéis contestado bien, y el {percentage_incorrects_first:.2f}% lo habéis contestado mal. ¡No os preocupéis! ¡Vamos a por la siguiente ronda!")    
print("Los resultados han sido guardados en 'results.txt'")
'''