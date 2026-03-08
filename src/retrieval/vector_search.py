"""Vector similarity search for document retrieval."""

from neo4j.exceptions import Neo4jError
from typing import List, Tuple
from src.embedding.ollama import embed_text
from src.config import VECTOR_INDEX_NAME, SEARCH_TOP_K, DATABASE_TIMEOUT
from src.logger_config import get_logger
from src.retrieval.database import get_driver

logger = get_logger("vector_search")

def retrieve(question: str, top_k: int = SEARCH_TOP_K) -> List[Tuple[str, float]]:
    """Retrieve relevant chunks using vector search with error handling"""
    driver = get_driver()  # Get shared driver instance
    
    if not question or not question.strip():
        logger.warning("Empty question provided for retrieval")
        return []
    
    try:
        logger.debug(f"Embedding question: {question[:50]}...")
        question_embedding = embed_text(question)
        
        if not question_embedding:
            logger.error("Failed to generate embedding for question")
            return []
        
        logger.debug(f"Searching for top {top_k} similar chunks")
        
        query = f"""
        CALL db.index.vector.queryNodes(
            '{VECTOR_INDEX_NAME}',
            $topK,
            $embedding
        )
        YIELD node, score
        RETURN node.text AS text, score
        """

        with driver.session() as session:
            result = session.run(
                query,
                topK=top_k,
                embedding=question_embedding
            )
            
            records = [(record["text"], record["score"]) for record in result]
            logger.info(f"Retrieved {len(records)} chunks (top_k={top_k})")
            return records
            
    except Neo4jError as e:
        logger.error(f"Database query failed: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Error during retrieval: {str(e)}")
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
