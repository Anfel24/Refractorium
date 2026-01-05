# src/llm_config.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def get_model():
    # Initialisation spécifique pour Gemini
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", # ou "gemini-1.5-pro"
        temperature=0,             # Important : 0 pour avoir des réponses stables en code
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )