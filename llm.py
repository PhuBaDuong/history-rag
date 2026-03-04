import requests
from config import OLLAMA_BASE_URL, OLLAMA_LLM_MODEL, OLLAMA_TEMPERATURE

OLLAMA_URL = f"{OLLAMA_BASE_URL}/api/generate"
MODEL_NAME = OLLAMA_LLM_MODEL

def generate_answer(context: str, question: str):
    prompt = f"""
        You are a history expert.

        Answer the question using ONLY the provided context.
        If the answer is not in the context, say "I don't know based on the provided text."

        Context:
        {context}

        Question:
        {question}

        Answer:
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "temperature": OLLAMA_TEMPERATURE
        }
    )

    response.raise_for_status()
    return response.json()["response"]