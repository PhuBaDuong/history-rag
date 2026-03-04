from neo4j import GraphDatabase
from embedder import embed_text
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, VECTOR_INDEX_NAME, SEARCH_TOP_K

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

def retrieve(question: str, top_k=SEARCH_TOP_K):
    question_embedding = embed_text(question)

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
        
        # for record in result:
        #     print("Text:", record["text"])
        #     print("Score:", record["score"])
        #     print("------")

        return [(record["text"], record["score"]) for record in result]