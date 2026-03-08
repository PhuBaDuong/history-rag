"""Embedding providers."""

from src.embedding.ollama import OllamaEmbedder, embed_text, get_embedder

__all__ = ["OllamaEmbedder", "embed_text", "get_embedder"]
