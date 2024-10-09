'''
Module dedicated to the evaluation of the answers provided by the devices M5Stick.
'''


def evaluar_respuestas(self, respuestas_correctas, respuestas_dispositivos):
    resultados = {}
    print(f"respuestas dispositivos: {respuestas_dispositivos}")

    for pregunta in respuestas_correctas:
                
        numero_pregunta = pregunta["question"]
        respuesta_correcta = pregunta["correct_answer"].lower()
        print(f"numero_pregunta: {numero_pregunta}")
        print(f"respuesta_correcta: {respuesta_correcta}") 
                
                
        if numero_pregunta in respuestas_dispositivos:

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
 

def save_results_to_file_teacher(filename, resultados_disp_especificos):
    with open(filename, "w") as file:
        file.write("Porcentajes de respuestas correctas/incorrectas por dispositivo:\n")
        for dispositivo, porcentajes in resultados_disp_especificos.items():
            file.write(f"Dispositivo {dispositivo}:\n")
            file.write(f"Porcentaje de respuestas correctas: {porcentajes['porcentaje_correctas']:.0f}%\n")
            file.write(f"Porcentaje de respuestas incorrectas: {porcentajes['porcentaje_incorrectas']:.0f}%\n\n")
    print(f"Los resultados han sido guardados en '{filename}'")     
        
