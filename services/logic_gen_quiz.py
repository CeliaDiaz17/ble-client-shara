'''
Uno de los módulos secundarios del sistema. Se encarga de la generacion de preguntas y respuestas del quiz, usando el modulo de OpenAI.
La generación del quiz se guarda en un archivo de texto mientras que las respuestas de SHARA no se almacenan en memoria.
'''

import fitz
import openai


def extract_text_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def generate_quiz(text, n_questions, n_choices, estructura_pregunta):
    prompt = f"Generate {n_questions} questions (in spanish) with {n_choices} answer choices based on the following text:\n\n{text}. Every question should start following this structure: {estructura_pregunta} Mark the correct answer with the symbol '*' next to it corresponding letter."
    
    response = openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        #model="gpt-3.5-turbo",
        model="gpt-4",

    )
    
    return response.choices[0].message.content.strip()

def generate_answers(quiz,text, estructura):
    prompt = f"Given the following quiz, answer every question with the correct choice (a, b, c). Then provide a brief explanation about why it is correct, base this explanation on this text:\n\n{text}. Use the structure: \n\n{estructura}. The quiz is as follows:\n\n{quiz}. Just follow the structure provided for all the answers."

    response = openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
                "temperature": 0.1,
            }
        ],
        #model="gpt-3.5-turbo", 
        model="gpt-4",
    )
    
    return response.choices[0].message.content.strip()

def main():

    estructura = "La respuesta correcta es [letra a/b/c]. [Breve explicación]."
    estructura_pregunta = "Pregunta[Numero que corresponda]: [Pregunta]."
    pdf_path = "/home/celia/Documents/mod1_TFG/tema_vertebrados_ESO.pdf"
    openai.api_key = "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" 
    pdf_content = extract_text_pdf(pdf_path)

    quiz = generate_quiz(pdf_content, 5, 3, estructura_pregunta)
    answers = generate_answers(quiz, pdf_content, estructura)
    
    with open("generated_quiz.txt", "w") as file:
        file.write(quiz)
    print("El cuestionario ha sido guardado en 'generated_quiz.txt'")
    
    with open("quiz_responses.txt", "w") as file:
        file.write(answers)
        
    print("Las respuestas han sido guardadas en 'quiz_reponses.txt'")
    
if __name__ == "__main__":
    main()