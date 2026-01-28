import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"Using API key: {api_key[:10]}...")

client = genai.Client(api_key=api_key)

print("\n📋 Listing all available models:")
try:
    # The response is a Pager - we need to iterate it
    models_pager = client.models.list()
    
    print("Available models:")
    for model in models_pager:
        print(f"  ✓ {model.name}")
        
except Exception as e:
    print(f"❌ Error: {e}")