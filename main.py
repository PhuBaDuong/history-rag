from retrieval.ingestion import ingest_book
from retrieval.vector_search import retrieve
from llm import generate_answer
from config import DOCUMENT_PATH, SKIP_INGESTION
from logger_config import get_logger

logger = get_logger("main")

def rag_pipeline(question: str):
    """Run RAG pipeline with error handling"""
    try:
        # 1️⃣ Retrieve relevant chunks
        logger.debug(f"Retrieving chunks for question: {question}")
        results = retrieve(question)
        
        if not results:
            logger.warning(f"No results found for question: {question}")
            return "No relevant information found in the knowledge base."

        # 2️⃣ Combine context
        context = "\n\n".join(
            [f"[Source {i+1} | score={score:.3f}]\n{text}"
             for i, (text, score) in enumerate(results)]
        )

        logger.debug(f"Retrieved {len(results)} chunks, generating answer...")
        print(context)

        # 3️⃣ Generate answer
        answer = generate_answer(context, question)
        logger.info(f"Answer generated successfully")
        return answer
        
    except Exception as e:
        logger.error(f"Error in RAG pipeline: {str(e)}")
        return f"Error processing question: {str(e)}"


if __name__ == "__main__":
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