import time
from gtts import gTTS
from playsound import playsound

def leer_archivo_resultados(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        resultados = file.read().strip()
    return resultados

def crear_audio(texto, nombre_archivo):
    tts = gTTS(texto, lang='es')
    tts.save(nombre_archivo)

def reproducir_audio(nombre_archivo):
    playsound(nombre_archivo)

def main():
    ruta_archivo_resultados = 'resultados_generales.txt'
    
    resultados = leer_archivo_resultados(ruta_archivo_resultados)
    
    # Crear y reproducir el audio de los resultados
    crear_audio(resultados, 'resultados.mp3')
    reproducir_audio('resultados.mp3')

if __name__ == '__main__':
    main()
