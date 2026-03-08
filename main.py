#!/usr/bin/env python3
"""
RAG System CLI Interface
Main entry point for the Retrieval-Augmented Generation system
"""

import sys
import os

# Add src to Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.retrieval.ingestion import ingest_book
from src.core.pipeline import rag_pipeline
from src.config import DOCUMENT_PATH, SKIP_INGESTION
from src.logger_config import get_logger

logger = get_logger("main")


def main():
    """Main entry point for RAG system."""
    logger.info("🚀 Starting RAG System")
    print("📚 Local History RAG System")
    print("Type 'exit' to quit.\n")

    # Load and ingest document if not skipped
    if not SKIP_INGESTION:
        print("📖 Loading document...")
        try:
            logger.info(f"Loading document from {DOCUMENT_PATH}")
            with open(DOCUMENT_PATH, "r") as f:
                book = f.read()
            
            if not book or not book.strip():
                logger.error(f"Document is empty: {DOCUMENT_PATH}")
                print("❌ Error: Document is empty")
                exit(1)
            
            print(f"✅ Document loaded ({len(book)} characters)")
            logger.info(f"Document loaded successfully ({len(book)} characters)")
            
            print("🔄 Ingesting document into vector database...")
            logger.info("Starting document ingestion...")
            ingest_book(book)
            print("✅ Ingestion complete!\n")
            logger.info("Ingestion completed successfully")
            
        except FileNotFoundError:
            logger.error(f"Document not found at {DOCUMENT_PATH}")
            print(f"❌ Error: Document not found at {DOCUMENT_PATH}")
            exit(1)
        except PermissionError:
            logger.error(f"Permission denied reading {DOCUMENT_PATH}")
            print(f"❌ Error: Permission denied reading {DOCUMENT_PATH}")
            exit(1)
        except Exception as e:
            logger.error(f"Failed to ingest document: {str(e)}")
            print(f"❌ Error: Failed to ingest document: {str(e)}")
            exit(1)
    else:
        logger.info("Skipping ingestion (SKIP_INGESTION=true)")
        print("⏭️  Skipping ingestion (SKIP_INGESTION=true)\n")

    logger.info("RAG system ready for queries")
    while True:
        try:
            question = input("Ask a question: ")
            if question.lower() in ["exit", "quit"]:
                logger.info("Exiting RAG system")
                print("Goodbye 👋")
                break

            response = rag_pipeline(question)

            print("\n🤖 Answer:\n")
            print(response)
            print("\n" + "="*60 + "\n")
            
        except KeyboardInterrupt:
            logger.info("User interrupted the program")
            print("\nGoodbye 👋")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {str(e)}")
            print(f"\n❌ Error: {str(e)}\n")


if __name__ == "__main__":
    main()