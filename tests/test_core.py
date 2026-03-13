"""Unit tests for RAG system core functionality."""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.pipeline import validate_question


class TestCoreValidation(unittest.TestCase):
    """Test suite for core validation functions."""
    
    def test_validate_question_valid(self):
        """Test valid question validation."""
        is_valid, error = validate_question("What is the history of Rome?")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
    
    def test_validate_question_empty(self):
        """Test empty question validation."""
        is_valid, error = validate_question("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())
    
    def test_validate_question_too_short(self):
        """Test question too short."""
        is_valid, error = validate_question("ab")
        self.assertFalse(is_valid)
        self.assertIn("least", error.lower())
    
    def test_validate_question_not_string(self):
        """Test non-string question."""
        is_valid, error = validate_question(123)
        self.assertFalse(is_valid)
        self.assertIn("text", error.lower())
    
    def test_validate_question_invalid_characters(self):
        """Test question with invalid characters."""
        is_valid, error = validate_question("What@#$%^&*()")
        self.assertFalse(is_valid)
        self.assertIn("invalid", error.lower())


class TestStepBack(unittest.TestCase):
    """Test suite for step-back prompting."""

    @patch("src.core.stepback.get_llm")
    def test_generate_stepback_success(self, mock_get_llm):
        """Test successful step-back question generation."""
        from src.core.stepback import generate_stepback

        mock_llm = MagicMock()
        mock_llm.generate.return_value = "What are the major military campaigns of Napoleon?"
        mock_get_llm.return_value = mock_llm

        result = generate_stepback("When did Napoleon invade Russia?")
        self.assertEqual(result, "What are the major military campaigns of Napoleon?")
        mock_llm.generate.assert_called_once()

    @patch("src.core.stepback.get_llm")
    def test_generate_stepback_strips_quotes(self, mock_get_llm):
        """Test that surrounding quotes are stripped from LLM response."""
        from src.core.stepback import generate_stepback

        mock_llm = MagicMock()
        mock_llm.generate.return_value = '"What is the history of Rome?"'
        mock_get_llm.return_value = mock_llm

        result = generate_stepback("When was Rome founded?")
        self.assertEqual(result, "What is the history of Rome?")

    @patch("src.core.stepback.get_llm")
    def test_generate_stepback_error_returns_original(self, mock_get_llm):
        """Test that LLM error falls back to original question."""
        from src.core.stepback import generate_stepback
        from src.utils.exceptions import LLMError

        mock_llm = MagicMock()
        mock_llm.generate.side_effect = LLMError("connection failed")
        mock_get_llm.return_value = mock_llm

        result = generate_stepback("When did Napoleon invade Russia?")
        self.assertEqual(result, "When did Napoleon invade Russia?")


if __name__ == "__main__":
    unittest.main()
