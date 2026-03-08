"""Abstract base class for LLM providers."""

from abc import ABC, abstractmethod


class LLMBase(ABC):
    """Base class for language model providers."""
    
    @abstractmethod
    def generate(self, context: str, question: str) -> str:
        """
        Generate an answer based on context and question.
        
        Args:
            context: Context text to base answer on
            question: User's question
            
        Returns:
            Generated answer string
            
        Raises:
            LLMError: If generation fails
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> dict:
        """Get information about the LLM."""
        pass
