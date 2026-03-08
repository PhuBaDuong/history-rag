"""Unit tests for retrieval functionality."""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.retrieval.vector_search import retrieve
from src.retrieval.ingestion import chunk_text


class TestRetrieval(unittest.TestCase):
    """Test suite for retrieval functions."""
    
    def test_chunk_text_basic(self):
        """Test basic text chunking."""
        text = "a" * 1000
        chunks = chunk_text(text, chunk_size=300, overlap=200)
        
        self.assertTrue(len(chunks) > 0)
        self.assertTrue(all(isinstance(c, str) for c in chunks))
    
    def test_chunk_text_empty(self):
        """Test chunking empty text."""
        chunks = chunk_text("", chunk_size=300, overlap=200)
        self.assertEqual(chunks, [])
    
    def test_chunk_text_small(self):
        """Test chunking small text."""
        text = "small"
        chunks = chunk_text(text, chunk_size=300, overlap=200)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], "small")
    
    @patch('src.retrieval.vector_search.embed_text')
    @patch('src.retrieval.vector_search.get_driver')
    def test_retrieve_empty_question(self, mock_driver, mock_embed):
        """Test retrieval with empty question."""
        result = retrieve("")
        self.assertEqual(result, [])
        mock_embed.assert_not_called()


if __name__ == "__main__":
    unittest.main()
