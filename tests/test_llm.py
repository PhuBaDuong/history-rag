"""Unit tests for LLM functionality."""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.llm.ollama import OllamaLLM
from src.utils.exceptions import LLMError


class TestLLM(unittest.TestCase):
    """Test suite for LLM functions."""
    
    @patch('src.llm.ollama.requests.post')
    def test_generate_answer_success(self, mock_post):
        """Test successful answer generation."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "This is the answer."}
        mock_post.return_value = mock_response
        
        llm = OllamaLLM()
        result = llm.generate("Context", "Question?")
        
        self.assertEqual(result, "This is the answer.")
        mock_post.assert_called_once()
    
    def test_generate_answer_empty_context(self):
        """Test answer generation with empty context."""
        llm = OllamaLLM()
        result = llm.generate("", "Question?")
        
        self.assertIn("No relevant", result)
    
    def test_generate_answer_empty_question(self):
        """Test answer generation with empty question."""
        llm = OllamaLLM()
        result = llm.generate("Context", "")
        
        self.assertIn("valid", result.lower())
    
    def test_get_model_info(self):
        """Test getting model info."""
        llm = OllamaLLM()
        info = llm.get_model_info()
        
        self.assertIn("provider", info)
        self.assertEqual(info["provider"], "ollama")
        self.assertIn("model", info)


if __name__ == "__main__":
    unittest.main()
