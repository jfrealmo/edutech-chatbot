import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import ollama

# --- Configuración ----------------------------------------------------------------

# Cargar variables de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

# --- Modelos de Datos -------------------------------------------------------------

class UserQuery(BaseModel):
    """Modelo para la pregunta que envía el usuario desde el frontend."""
    question: str

# --- Inicialización de FastAPI ----------------------------------------------------

app = FastAPI()

# --- Endpoints de la API ----------------------------------------------------------

@app.get("/")
async def read_root():
    """Endpoint raíz para verificar que el backend está funcionando."""
    return {"status": "backend listo"}

@app.post("/api/ask-llm")
async def ask_llm(query: UserQuery):
    """
    Endpoint principal para recibir preguntas y obtener respuestas del LLM.
    Si se proporciona una OPENAI_API_KEY, se usará OpenAI.
    De lo contrario, se usará Ollama como respaldo para desarrollo.
    """
    use_openai = OPENAI_API_KEY and OPENAI_API_KEY.strip() != ""

    try:
        if use_openai:
            # --- Lógica para OpenAI ---
            print("Usando proveedor: OpenAI")
            openai.api_key = OPENAI_API_KEY
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente educativo. Responde de forma concisa y útil."},
                    {"role": "user", "content": query.question}
                ]
            )
            return {"answer": response.choices[0].message.content}

        else:
            # --- Lógica para Ollama (Fallback) ---
            print(f"Usando proveedor: Ollama (URL: {OLLAMA_API_URL})")
            client = ollama.Client(host=OLLAMA_API_URL)
            response = client.chat(
                model=OLLAMA_MODEL,
                messages=[
                    {"role": "system", "content": "Eres un asistente educativo. Responde de forma concisa y útil."},
                    {'role': 'user', 'content': query.question},
                ]
            )
            return {"answer": response['message']['content']}

    except Exception as e:
        # Manejo de errores genérico para cualquier problema con los LLM
        error_message = f"Error al procesar la solicitud del LLM: {str(e)}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)
