'''
Module dedicated to the evaluation of the answers provided by the devices M5Stick.
'''


def get_corrects(json_data, devices_responses, question_number):
    question_key = str(question_number)
    correct_answ = json_data[question_key]["correct"]
    print(f"correct_answ en data evaluation: {correct_answ}")
    corrects = 0
    
    for response in devices_responses:
        #for response in responses:
            if response.lower() == correct_answ:
                corrects += 1
    
    return corrects        
    

def calculate_percent(correct_answ, total_answ):
    print(total_answ)
    if total_answ == 0:
        return 0,100 #para no dividir entre 0 y que pete
        
    percentage_correct = (correct_answ / total_answ) * 100
    #percentage_incorrect = 100 - percentage_correct
        
    return percentage_correct


'''
MICKY HERRAMIENTAS QUE USAREMOS MAS TARDE
*Calculo de porcentajes específicos y desde que dispositivo provienen. Se guarda en un txt para dispo del profe*

Si se usa modificar para archivo json

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


'''