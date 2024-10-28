'''
OpenAI wrapper for making the request to the API 
'''

import openai
from typing import Dict, Any
import os

   
api_key = os.getenv("OPENAI_API_KEY")
    
def make_request(prompt):
    response = openai.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-4o-mini",  
)     
    full_output = response.choices[0].message.content.strip()
    return full_output

        
        

    