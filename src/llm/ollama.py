"""Ollama LLM provider implementation."""

import requests
import time
from src.llm.base import LLMBase
from src.utils.exceptions import LLMError
from src.config import OLLAMA_BASE_URL, OLLAMA_LLM_MODEL, OLLAMA_TEMPERATURE, LLM_TIMEOUT, RETRY_DELAY
from src.logger_config import get_logger

logger = get_logger("llm")

MAX_RETRIES = 2


class OllamaLLM(LLMBase):
    """Ollama LLM provider."""
    
    def __init__(self, base_url: str = None, model: str = None, temperature: float = None, timeout: int = None):
        """
        Initialize Ollama LLM.
        
        Args:
            base_url: Ollama base URL (uses config default if not provided)
            model: Model name (uses config default if not provided)
            temperature: Temperature parameter (uses config default if not provided)
            timeout: Request timeout in seconds (uses config default if not provided)
        """
        self.base_url = base_url or OLLAMA_BASE_URL
        self.model = model or OLLAMA_LLM_MODEL
        self.temperature = temperature if temperature is not None else OLLAMA_TEMPERATURE
        self.timeout = timeout or LLM_TIMEOUT
        self.url = f"{self.base_url}/api/generate"
    
    def generate(self, context: str, question: str) -> str:
        """Generate answer using LLM with error handling."""
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
                    self.url,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "temperature": self.temperature
                    },
                    timeout=self.timeout
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
                error_msg = f"Cannot connect to LLM service at {self.base_url}"
                logger.error(error_msg)
                return f"Cannot connect to LLM service. Make sure Ollama is running at {self.base_url}"
                
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error from LLM: {e.response.status_code}")
                return "Error generating answer - service error."
                
            except KeyError:
                logger.error("Invalid response from LLM - missing 'response' key")
                return "Error: Invalid response from language model."
                
            except Exception as e:
                logger.error(f"Unexpected error during answer generation: {str(e)}")
                return f"Error generating answer: {str(e)}"
    
    def get_model_info(self) -> dict:
        """Get information about the LLM."""
        return {
            "provider": "ollama",
            "model": self.model,
            "base_url": self.base_url,
            "temperature": self.temperature,
            "timeout": self.timeout
        }


# Global singleton instance
_llm = None


def get_llm() -> OllamaLLM:
    """Get or create the global LLM instance."""
    global _llm
    if _llm is None:
        _llm = OllamaLLM()
    return _llm


def generate_answer(context: str, question: str) -> str:
    """Convenience function for generating answers."""
    return get_llm().generate(context, question)
