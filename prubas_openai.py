# test_openai_api.py
import os
import openai
from services.cloud.openai_api import OpenAIAPI

def main():
    # Clave API de prueba (cambiar por tu clave válida)
    api_key = os.getenv("OPENAI_API_KEY")
    openai_api = OpenAIAPI(api_key)
    
    # Probar el método para generar quiz y respuestas
    print("Probando generate_quiz_with_answers...")
    try:
        # Este método generará el quiz y las respuestas, las separará y las guardará en los archivos .txt
        openai_api.generate_quiz_with_answers()

        print("Quiz y respuestas generados correctamente y guardados en archivos separados.")
        print("Verifica los archivos 'generated_quiz.txt' y 'quiz_responses.txt'.")
        
    except Exception as e:
        print(f"Error en generate_quiz_with_answers: {e}")
        
    # Probar el método para generar mensajes motivacionales basados en porcentajes
    print("\nProbando generate_possible_answ...")
    try:
        possible_answ = openai_api.generate_possible_answ(75, 25)
        print("Mensajes motivacionales generados correctamente:")
        print(possible_answ)
    except Exception as e:
        print(f"Error en generate_possible_answ: {e}")

if __name__ == "__main__":
    main()

