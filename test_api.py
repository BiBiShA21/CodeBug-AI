import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ API KEY NOT FOUND! Check your .env file")
else:
    print(f"✅ API Key found: {API_KEY[:10]}...")
    genai.configure(api_key=API_KEY)
    
    # List all available models
    print("\n📋 Available Models:")
    for model in genai.list_models():
        print(f"  - {model.name}")