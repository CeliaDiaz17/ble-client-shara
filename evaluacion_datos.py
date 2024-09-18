import queue
import json
import os

def leer_respuestas_correctas(correct_answers):
    with open (correct_answers, "r") as file:
        data = json.load(file)
    return data

def guardar_respuestas_dir(directorio):
    respuestas = {}
    for archivo in os.listdir(directorio):
        print(f"Procesando archivo: {archivo}")
        if archivo.endswith(".json"):
            numero_pregunta = archivo.split("_")[2].split(".")[0]
            with open(os.path.join(directorio, archivo), "r") as file:
                respuestas[numero_pregunta] = json.load(file)
        else:
            print(f"Aviso: el archivo {archivo} ha sido ignorado.")
    return respuestas

def evaluar_respuestas(respuestas_correctas, respuestas_dispositivos):
    resultados = {}
    for pregunta in respuestas_correctas:
        numero_pregunta = pregunta["question"]
        respuesta_correcta = pregunta["correct_answer"].lower()
        print(f"numero_pregunta: {numero_pregunta}")
        print(f"respuesta_correcta: {respuesta_correcta}") 
        
        
        if numero_pregunta in respuestas_dispositivos:
            #aqui no entra
            respuestas_pregunta = respuestas_dispositivos[numero_pregunta]
            resultados[numero_pregunta] = {
                'respuesta_correcta': respuesta_correcta,
                'respuestas_dispositivos': {},
            }
            
            for dispositivo, respuestas in respuestas_pregunta.items():
                respuesta_dispositivo = respuestas[0].lower() if respuestas else ''
                es_correcta = respuesta_dispositivo == respuesta_correcta
                resultados[numero_pregunta]['respuestas_dispositivos'][dispositivo] = es_correcta
        else:
            print(f"Las respuestas para la pregunta {numero_pregunta} no se han encontrado.")
    return resultados

def calculo_porcentajes(resultados):
    total_respuestas = 0
    total_correctas = 0
    
    for resultado in resultados.values():
        for es_correcta in resultado["respuestas_dispositivos"].values():
            total_respuestas += 1
            if es_correcta:
                total_correctas += 1
    
    porcentaje_correctas = (total_correctas / total_respuestas) * 100
    porcentaje_incorrectas = 100 - porcentaje_correctas
    
    return porcentaje_correctas, porcentaje_incorrectas

def calculo_porcentajes_especificos(resultados):
    estadisticas_dispositivos = {}

    for resultado in resultados.values():
        for dispositivo, es_correcta in resultado["respuestas_dispositivos"].items():
            if dispositivo not in estadisticas_dispositivos:
                estadisticas_dispositivos[dispositivo] = {
                    "correctas": 0,
                    "incorrectas": 0,
                    "total": 0,
                }
            estadisticas_dispositivos[dispositivo]["total"] += 1
            if es_correcta:
                estadisticas_dispositivos[dispositivo]["correctas"] += 1
            else:
                estadisticas_dispositivos[dispositivo]["incorrectas"] += 1

    porcentajes = {}
    for dispositivo, stats in estadisticas_dispositivos.items():
        porcentaje_correctas = (stats["correctas"] / stats["total"]) * 100
        porcentaje_incorrectas = (stats["incorrectas"] / stats["total"]) * 100
        porcentajes[dispositivo] = {
            "porcentaje_correctas": porcentaje_correctas,
            "porcentaje_incorrectas": porcentaje_incorrectas,
        }

    return porcentajes
        

def imprimir_resultados(resultados, correctas, incorrectas, correctas_disp):
    #Porcentajes correcto/incorrecto de cada pregunta
    for numero_pregunta, resultado in resultados.items():
        respuesta_correcta = resultado["respuesta_correcta"]
        print(f"Respuesta correcta para la pregunta {numero_pregunta}: {respuesta_correcta}")
        print("Resultados:")
        for dispositivo, es_correcta in resultado["respuestas_dispositivos"].items():
            print(f"Dispositivo {dispositivo}: {'Correcta' if es_correcta else 'Incorrecta'}")
        print()
        
    #Porcentaje de respuestas correctas/incorrectas
    print(f"Porcentaje general de respuestas correctas: {correctas:.0f}%")
    print(f"Porcentaje general de respuestas incorrectas: {incorrectas:.0f}%")
    
    #Porcentajes de respuestas correctas/incorrectas por dispositivo
    print("Porcentajes de respuestas correctas/incorrectas por dispositivo:")
    for dispositivo, porcentajes in correctas_disp.items():
        print(f"Dispositivo {dispositivo}:")
        print(f"Porcentaje de respuestas correctas: {porcentajes['porcentaje_correctas']:.0f}%")
        print(f"Porcentaje de respuestas incorrectas: {porcentajes['porcentaje_incorrectas']:.0f}%")
        print()
    
'''
def save_results_to_file(filename, results):
    with open(filename, "w") as file:
        for i, (percentage_corrects, percentage_incorrects) in enumerate(results, 1):
            #file.write(f"Ronda {i}:\n")
            file.write(f"Bueno chicos, el: {percentage_corrects:.0f}% de vosotros lo habéis contestado bien, y el {percentage_incorrects:.0f}% lo habéis contestado mal. ¡No os preocupéis! ¡Vamos a por la siguiente ronda!\n\n")    
    print(f"Los resultados han sido guardados en '{filename}'")
'''

def main ():
    archivo_correct_answers = "correct_answers.json"
    directorio_respuestas = "respuestas"
    
    respuestas_correctas = leer_respuestas_correctas(archivo_correct_answers)
    respuestas_dispositivos = guardar_respuestas_dir(directorio_respuestas)

    resultados = evaluar_respuestas(respuestas_correctas, respuestas_dispositivos)
    porcentaje_correctas, porcentaje_incorrectas = calculo_porcentajes(resultados)
    porcentajes_especificos = calculo_porcentajes_especificos(resultados)
    imprimir_resultados(resultados, porcentaje_correctas, porcentaje_incorrectas,porcentajes_especificos)
    
if __name__ == "__main__":
    main()
