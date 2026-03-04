from neo4j import GraphDatabase
from embedder import embed_text
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, CHUNK_SIZE, CHUNK_OVERLAP

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i+chunk_size])
    return chunks

def store_chunk(tx, chunk_id, text, embedding):
    tx.run("""
        CREATE (c:Chunk {
            id: $id,
            text: $text,
            embedding: $embedding
        })
    """, id=chunk_id, text=text, embedding=embedding)

def ingest_book(book_text):
    chunks = chunk_text(book_text)

    with driver.session() as session:
        for i, chunk in enumerate(chunks):
            embedding = embed_text(chunk)
            session.execute_write(store_chunk, i, chunk, embedding)

    print("Ingestion completed.")