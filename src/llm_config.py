import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_model():
    api_key = os.getenv("GOOGLE_API_KEY")
    
    

    # Utilise un modèle compatible avec v1beta
    return ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash",  # PAS de -latest, juste le nom de base
        google_api_key=api_key,
        temperature=0,
       
    )

