"""
Configuration management for RAG system
Loads settings from environment variables with sensible defaults
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# NEO4J DATABASE CONFIGURATION
# ============================================
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# ============================================
# OLLAMA (LLM & EMBEDDINGS) CONFIGURATION
# ============================================
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
OLLAMA_LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "qwen3.5:9b")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.2"))

# ============================================
# DOCUMENT INGESTION CONFIGURATION
# ============================================
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "300"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
DOCUMENT_PATH = os.getenv("DOCUMENT_PATH", "data/history.txt")

# ============================================
# VECTOR SEARCH CONFIGURATION
# ============================================
VECTOR_INDEX_NAME = os.getenv("VECTOR_INDEX_NAME", "chunk_embedding_index")
SEARCH_TOP_K = int(os.getenv("SEARCH_TOP_K", "5"))

# ============================================
# LOGGING CONFIGURATION
# ============================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/rag_system.log")

# ============================================
# APPLICATION CONFIGURATION
# ============================================
SKIP_INGESTION = os.getenv("SKIP_INGESTION", "false").lower() == "true"
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
