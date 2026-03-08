"""Document ingestion into vector database."""

from neo4j.exceptions import Neo4jError
from typing import List, Any
from src.embedding.ollama import embed_text
from src.config import NEO4J_URI, CHUNK_SIZE, CHUNK_OVERLAP, VECTOR_INDEX_NAME
from src.logger_config import get_logger
from src.retrieval.database import get_driver, create_vector_index

logger = get_logger("ingestion")

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping chunks"""
    if not text:
        logger.warning("Empty text provided for chunking")
        return []
    
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i+chunk_size])
    
    logger.info(f"Created {len(chunks)} chunks from text ({len(text)} characters)")
    return chunks

def store_chunk(tx: Any, chunk_id: int, text: str, embedding: List[float]) -> None:
    """Store a single chunk in Neo4j"""
    tx.run("""
        CREATE (c:Chunk {
            id: $id,
            text: $text,
            embedding: $embedding
        })
    """, id=chunk_id, text=text, embedding=embedding)

def ingest_book(book_text: str) -> None:
    """Ingest book text into vector database with error handling"""
    driver = get_driver()  # Get shared driver instance
    
    try:
        # Verify connection
        logger.info(f"Connecting to Neo4j at {NEO4J_URI}")
        with driver.session() as session:
            session.run("RETURN 1")
        logger.info("✅ Database connection verified")
        
    except Neo4jError as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise Exception(f"Cannot connect to Neo4j: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during database check: {str(e)}")
        raise
    
    try:
        # Chunk the text
        chunks = chunk_text(book_text)
        if not chunks:
            logger.error("No chunks created from text")
            return
        
        # Create vector index (if it doesn't exist)
        logger.info(f"Ensuring vector index exists: {VECTOR_INDEX_NAME}")
        if not create_vector_index(VECTOR_INDEX_NAME):
            logger.error(f"Failed to create vector index: {VECTOR_INDEX_NAME}")
            raise Exception(f"Cannot create vector index: {VECTOR_INDEX_NAME}")
        logger.info(f"✅ Vector index ready: {VECTOR_INDEX_NAME}")
        
        # Ingest chunks
        logger.info("Starting document ingestion...")
        with driver.session() as session:
            for i, chunk in enumerate(chunks):
                try:
                    logger.debug(f"Processing chunk {i + 1}/{len(chunks)}")
                    embedding = embed_text(chunk)
                    session.execute_write(store_chunk, i, chunk, embedding)
                    
                    if (i + 1) % 10 == 0:
                        logger.info(f"Ingested {i + 1}/{len(chunks)} chunks")
                        
                except Exception as e:
                    logger.error(f"Failed to ingest chunk {i}: {str(e)}")
                    raise
        
        logger.info("✅ Document ingestion completed successfully")
        
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        raise
