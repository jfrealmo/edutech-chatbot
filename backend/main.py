import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import ollama

# --- Configuración ----------------------------------------------------------------

# Cargar variables de entorno
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

# Validaciones iniciales
if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
    raise ValueError("La variable de entorno OPENAI_API_KEY es necesaria cuando LLM_PROVIDER es 'openai'")

# Configurar el cliente de OpenAI si es necesario
if LLM_PROVIDER == "openai":
    openai.api_key = OPENAI_API_KEY

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
    Endpoint principal para recibir preguntas y obtener respuestas del LLM configurado.
    """
    try:
        if LLM_PROVIDER == "openai":
            # --- Lógica para OpenAI ---
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # O el modelo que prefieras
                messages=[
                    {"role": "system", "content": "Eres un asistente educativo. Responde de forma concisa y útil."},
                    {"role": "user", "content": query.question}
                ]
            )
            return {"answer": response.choices[0].message['content']}

        elif LLM_PROVIDER == "ollama":
            # --- Lógica para Ollama ---
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[
                    {"role": "system", "content": "Eres un asistente educativo. Responde de forma concisa y útil."},
                    {'role': 'user', 'content': query.question},
                ],
                # Configurar el cliente para apuntar a la URL correcta
                # Nota: La librería de Python de Ollama puede que no soporte `host` directamente
                # en la función `chat`. Se configura globalmente o se asume localhost.
                # La conexión se gestionará a través de la URL base del cliente si es necesario.
            )
            return {"answer": response['message']['content']}

        else:
            raise HTTPException(status_code=500, detail="Proveedor de LLM no configurado correctamente.")

    except Exception as e:
        # Manejo de errores genérico para cualquier problema con los LLM
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud del LLM: {str(e)}")

# --- Lógica adicional para configurar el cliente de Ollama si es necesario ---
# Algunas versiones de la librería `ollama` pueden requerir configurar el cliente explícitamente.
# Si la URL de OLLAMA no es localhost, podrías necesitar algo como:
# ollama.Client(host=OLLAMA_API_URL)
# Por ahora, la implementación estándar asume que la URL se puede gestionar por defecto.

