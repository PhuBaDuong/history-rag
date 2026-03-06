import requests
from config import OLLAMA_BASE_URL, OLLAMA_EMBEDDING_MODEL
from logger_config import get_logger

logger = get_logger("embedder")
OLLAMA_URL = f"{OLLAMA_BASE_URL}/api/embeddings"
MODEL_NAME = OLLAMA_EMBEDDING_MODEL

MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

def embed_text(text: str):
    """Generate embeddings for text with error handling and retry logic"""
    if not text or not text.strip():
        logger.warning("Empty text provided for embedding")
        return []
    
    for attempt in range(MAX_RETRIES):
        try:
            logger.debug(f"Embedding text (attempt {attempt + 1}/{MAX_RETRIES})")
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": text
                },
                timeout=30
            )
            response.raise_for_status()
            embedding = response.json()["embedding"]
            logger.debug(f"Successfully embedded text (dimension: {len(embedding)})")
            return embedding
            
        except requests.exceptions.Timeout:
            logger.warning(f"Embedding request timeout (attempt {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                import time
                time.sleep(RETRY_DELAY)
            else:
                logger.error("Embedding failed: Max retries exceeded due to timeout")
                raise
                
        except requests.exceptions.ConnectionError as e:
            logger.warning(f"Connection error to Ollama (attempt {attempt + 1}/{MAX_RETRIES}): {str(e)}")
            if attempt < MAX_RETRIES - 1:
                import time
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Embedding failed: Cannot connect to Ollama at {OLLAMA_BASE_URL}")
                raise
                
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error from Ollama: {e.response.status_code} - {e.response.text}")
            raise
            
        except KeyError:
            logger.error(f"Invalid response from Ollama - missing 'embedding' key")
            raise
            
        except Exception as e:
            logger.error(f"Unexpected error during embedding: {str(e)}")
            raise

