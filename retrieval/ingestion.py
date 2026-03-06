from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError
from embedder import embed_text
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, CHUNK_SIZE, CHUNK_OVERLAP
from logger_config import get_logger

logger = get_logger("ingestion")

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks"""
    if not text:
        logger.warning("Empty text provided for chunking")
        return []
    
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i+chunk_size])
    
    logger.info(f"Created {len(chunks)} chunks from text ({len(text)} characters)")
    return chunks

def store_chunk(tx, chunk_id, text, embedding):
    """Store a single chunk in Neo4j"""
    tx.run("""
        CREATE (c:Chunk {
            id: $id,
            text: $text,
            embedding: $embedding
        })
    """, id=chunk_id, text=text, embedding=embedding)

def ingest_book(book_text):
    """Ingest book text into vector database with error handling"""
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
    finally:
        # Always close the driver
        driver.close()
        logger.debug("Database driver closed")