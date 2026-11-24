import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. .env faylını tapır və API açarını yükləyir
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

client = genai.Client()

SYSTEM_PROMPT = """
Sən Bakıda keçirilən hakatona hazırlaşan təcrübəli AI mühəndisi köməkçisisən.
İstifadəçinin suallarına qısa, konkret və praktiki nümunələrlə cavab ver.
"""

def ask_agent(user_message: str):
    # Yeni açarlar üçün aktiv olan modellər
    models = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash"]
    
    for model_name in models:
        for attempt in range(3):  # Hər model üçün 3 dəfə cəhd edir
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=user_message,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.4,
                    ),
                )
                print(f"\n✅ Cavab ({model_name}):\n")
                print(response.text)
                return
            except Exception as e:
                print(f"⏳ {model_name} (Cəhd {attempt+1}/3) yüklüdür, 4 saniyə gözlənilir...")
                time.sleep(4)

    print("❌ Serverlər hazırda çox yüklüdür, 1 dəqiqə sonra yenidən yoxla.")

if __name__ == "__main__":
    sual = input("Agentə sualını yaz: ")
    ask_agent(sual)