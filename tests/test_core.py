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


if __name__ == "__main__":
    unittest.main()
