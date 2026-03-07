import requests
import time
from config import OLLAMA_BASE_URL, OLLAMA_LLM_MODEL, OLLAMA_TEMPERATURE, LLM_TIMEOUT, RETRY_DELAY
from logger_config import get_logger

logger = get_logger("llm")
OLLAMA_URL = f"{OLLAMA_BASE_URL}/api/generate"
MODEL_NAME = OLLAMA_LLM_MODEL

MAX_RETRIES = 2

def generate_answer(context: str, question: str) -> str:
    """Generate answer using LLM with error handling"""
    if not context or not context.strip():
        logger.warning("No context provided for answer generation")
        return "No relevant information found to answer your question."
    
    if not question or not question.strip():
        logger.error("Empty question provided")
        return "Please ask a valid question."
    
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

    for attempt in range(MAX_RETRIES):
        try:
            logger.debug(f"Generating answer (attempt {attempt + 1}/{MAX_RETRIES})")
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": OLLAMA_TEMPERATURE
                },
                timeout=LLM_TIMEOUT
            )
            response.raise_for_status()
            answer = response.json()["response"]
            logger.info("Answer generated successfully")
            return answer
            
        except requests.exceptions.Timeout:
            logger.warning(f"LLM request timeout (attempt {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                logger.error("Answer generation failed: Service timeout")
                return "Unable to generate answer - service timeout. Please try again."
                
        except requests.exceptions.ConnectionError:
            logger.error(f"Cannot connect to LLM service at {OLLAMA_BASE_URL}")
            return f"Cannot connect to LLM service. Make sure Ollama is running at {OLLAMA_BASE_URL}"
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error from LLM: {e.response.status_code}")
            return "Error generating answer - service error."
            
        except KeyError:
            logger.error("Invalid response from LLM - missing 'response' key")
            return "Error: Invalid response from language model."
            
        except Exception as e:
            logger.error(f"Unexpected error during answer generation: {str(e)}")
            return f"Error generating answer: {str(e)}"