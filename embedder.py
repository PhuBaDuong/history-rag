import requests
from config import OLLAMA_BASE_URL, OLLAMA_EMBEDDING_MODEL

OLLAMA_URL = f"{OLLAMA_BASE_URL}/api/embeddings"
MODEL_NAME = OLLAMA_EMBEDDING_MODEL

def embed_text(text: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": text
        }
    )

    response.raise_for_status()
    return response.json()["embedding"]

