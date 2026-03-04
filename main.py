from retrieval.ingestion import ingest_book
from retrieval.vector_search import retrieve
from llm import generate_answer
from config import DOCUMENT_PATH, SKIP_INGESTION

def rag_pipeline(question: str):
    # 1️⃣ Retrieve relevant chunks
    results = retrieve(question)

    # 2️⃣ Combine context
    context = "\n\n".join(
    [f"[Source {i+1} | score={score:.3f}]\n{text}"
     for i, (text, score) in enumerate(results)]
)

    print(context)

    # 3️⃣ Generate answer
    answer = generate_answer(context, question)

    return answer


if __name__ == "__main__":
    print("📚 Local History RAG System")
    print("Type 'exit' to quit.\n")

    # Load and ingest document if not skipped
    if not SKIP_INGESTION:
        print("📖 Loading document...")
        try:
            with open(DOCUMENT_PATH, "r") as f:
                book = f.read()
            print(f"✅ Document loaded ({len(book)} characters)")
            print("🔄 Ingesting document into vector database...")
            ingest_book(book)
            print("✅ Ingestion complete!\n")
        except FileNotFoundError:
            print(f"❌ Error: Document not found at {DOCUMENT_PATH}")
            exit(1)
    else:
        print("⏭️  Skipping ingestion (SKIP_INGESTION=true)\n")

    while True:
        question = input("Ask a question: ")
        if question.lower() in ["exit", "quit"]:
            print("Goodbye 👋")
            break

        response = rag_pipeline(question)

        print("\n🤖 Answer:\n")
        print(response)
        print("\n" + "="*60 + "\n")