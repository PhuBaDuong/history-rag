#!/usr/bin/env python3
"""
Document Ingestion Script
Standalone ingestion of documents into the vector database
Run separately from the main RAG query interface
"""

import sys
import os

# Add src to Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.retrieval.ingestion import ingest_book
from src.config import DOCUMENT_PATH
from src.logger_config import get_logger

logger = get_logger("ingest")


def main():
    """Ingest document into vector database."""
    logger.info("🚀 Starting Document Ingestion")
    print("📚 RAG Document Ingestion Tool")
    print("="*60)
    
    try:
        # Load document
        print(f"\n📖 Loading document from: {DOCUMENT_PATH}")
        logger.info(f"Loading document from {DOCUMENT_PATH}")
        
        with open(DOCUMENT_PATH, "r") as f:
            book = f.read()
        
        if not book or not book.strip():
            logger.error(f"Document is empty: {DOCUMENT_PATH}")
            print("❌ Error: Document is empty")
            return 1
        
        print(f"✅ Document loaded ({len(book)} characters)")
        logger.info(f"Document loaded successfully ({len(book)} characters)")
        
        # Ingest document
        print("\n🔄 Ingesting document into vector database...")
        logger.info("Starting document ingestion...")
        ingest_book(book)
        
        print("✅ Ingestion complete!")
        logger.info("Ingestion completed successfully")
        print("="*60 + "\n")
        return 0
        
    except FileNotFoundError:
        logger.error(f"Document not found at {DOCUMENT_PATH}")
        print(f"❌ Error: Document not found at {DOCUMENT_PATH}")
        return 1
    except PermissionError:
        logger.error(f"Permission denied reading {DOCUMENT_PATH}")
        print(f"❌ Error: Permission denied reading {DOCUMENT_PATH}")
        return 1
    except Exception as e:
        logger.error(f"Failed to ingest document: {str(e)}")
        print(f"❌ Error: Failed to ingest document: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
