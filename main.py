#!/usr/bin/env python3
"""
RAG System CLI Interface
Main entry point for Retrieval-Augmented Generation queries
Document ingestion is handled separately by ingest.py
"""

import sys
import os

# Add src to Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.pipeline import rag_pipeline
from src.logger_config import get_logger

logger = get_logger("main")


def main():
    """Main entry point for RAG system - query interface only."""
    logger.info("🚀 Starting RAG System")
    print("📚 Local History RAG System")
    print("(Use 'ingest.py' to load documents)")
    print("Type 'exit' to quit.\n")

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