import os
from dotenv import load_dotenv
# import google.generativeai as genai
from agent import Agent

load_dotenv()

print("🚀 Primer agente de IA")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: No se encontró la GEMINI_API_KEY")
else:
    agent = Agent(api_key)

    while True:
        user_input = input("\nTú: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ("salir", "exit", "bye", "sayonara"):
            print("Hasta luego!")
            break
        
        # En Gemini, el historial y las herramientas se procesan aquí
        try:
            respuesta = agent.ask(user_input)
            print(f"Asistente: {respuesta}")
        except Exception as e:
            print(f"⚠️ Error: {e}")