import time
from gtts import gTTS
from playsound import playsound

def leer_archivo_preguntas(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        preguntas = file.read().strip().split('\n\n')
    return preguntas

def leer_archivo_evaluaciones(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        evaluaciones = file.read().strip().split('\n')
    return evaluaciones

def leer_archivo_respuestas(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        respuestas = file.read().strip().split('\n')
    return respuestas                                            

def crear_audio(texto, nombre_archivo):
    tts = gTTS(texto, lang='es')
    tts.save(nombre_archivo)

def reproducir_audio(nombre_archivo):
    playsound(nombre_archivo)

def main():
    ruta_archivo_preguntas = '/home/celia/Documents/mod1_TFG/generated_quiz.txt'
    ruta_archivo_evaluaciones = '/home/celia/Documents/mod1_TFG/results.txt'
    ruta_archivo_respuestas = '/home/celia/Documents/mod1_TFG/quiz_responses.txt'
    
    preguntas = leer_archivo_preguntas(ruta_archivo_preguntas)
    evaluaciones = leer_archivo_evaluaciones(ruta_archivo_evaluaciones)
    respuestas = leer_archivo_respuestas(ruta_archivo_respuestas)
    
    for i, pregunta in enumerate(preguntas):
        # Parte de la pregunta y opciones
        crear_audio(pregunta, 'pregunta.mp3')
        reproducir_audio('pregunta.mp3')
        
        # Pausa de 15 segundos para que los niños contesten
        time.sleep(15)
        
        # Parte de la respuesta correcta y explicación
        respuesta_correcta = respuestas[i]
        crear_audio(respuesta_correcta, 'respuesta.mp3')
        reproducir_audio('respuesta.mp3')
        
        # Evaluación
        evaluacion = evaluaciones[i]
        crear_audio(evaluacion, 'evaluacion.mp3')
        reproducir_audio('evaluacion.mp3')
        
        # Pausa de 3 segundos antes de la siguiente pregunta
        time.sleep(3)

if __name__ == '__main__':
    main()






































'''
from gtts import gTTS
from playsound import playsound
import os
import time

def leer_texto_en_alto(archivo, resultados):
    # Leer el contenido del archivo de resultados
    with open(resultados, 'r', encoding='utf-8') as f:
        contenido_resultados = f.read()

    # Leer el contenido del archivo de preguntas y respuestas
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Eliminar el símbolo "*"
    contenido = contenido.replace('*', '')
    
    # Dividir el texto en secciones numeradas de preguntas y explicaciones
    secciones = contenido.split('\n\n')

    # Procesar cada sección (pregunta y su explicación)
    for seccion in secciones:
        # Asegurarse de que la sección no esté vacía y normalizarla
        if seccion.strip():
            texto = ' '.join(seccion.strip().split('\n'))
            
            # Crear un objeto gTTS con el texto de la pregunta y explicación
            tts = gTTS(text=texto, lang='es')
            
            # Guardar el archivo de audio
            archivo_audio = 'audio.mp3'
            tts.save(archivo_audio)
            
            # Reproducir el archivo de audio
            playsound(archivo_audio)
            
            # Eliminar el archivo de audio después de reproducirlo
            os.remove(archivo_audio)
            
            # Pausa de 5 segundos entre secciones
            time.sleep(3)
            
            # Crear un objeto gTTS con el contenido de resultados
            tts_resultados = gTTS(text=contenido_resultados, lang='es')
            
            # Guardar el archivo de audio
            archivo_audio_resultados = 'audio_resultados.mp3'
            tts_resultados.save(archivo_audio_resultados)
            
            # Reproducir el archivo de audio
            playsound(archivo_audio_resultados)
            
            # Eliminar el archivo de audio después de reproducirlo
            os.remove(archivo_audio_resultados)
            
            # Pausa de 5 segundos entre secciones
            time.sleep(8)

# Llamar a la función con el nombre del archivo .txt y resultados
archivo = '/home/celia/Documents/mod1_TFG/generated_quiz.txt'
resultados = '/home/celia/Documents/mod1_TFG/results.txt'
leer_texto_en_alto(archivo, resultados)
'''
