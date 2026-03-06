from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError
from embedder import embed_text
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, VECTOR_INDEX_NAME, SEARCH_TOP_K
from logger_config import get_logger

logger = get_logger("vector_search")

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

def retrieve(question: str, top_k=SEARCH_TOP_K):
    """Retrieve relevant chunks using vector search with error handling"""
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
        return []