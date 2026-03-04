# 📚 Local History RAG System

A **Retrieval-Augmented Generation (RAG)** system that answers historical questions by retrieving relevant context from source documents and generating answers using an LLM.

## 🎯 What is RAG?

RAG combines two powerful capabilities:
1. **Retrieval** - Finds relevant document chunks based on semantic similarity
2. **Generation** - Uses an LLM to generate answers grounded in retrieved context

This approach improves accuracy and allows the system to cite sources.

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│  User Question                          │
└────────────────┬────────────────────────┘
                 │
        ┌────────▼─────────┐
        │  Vector Search   │  (semantic similarity)
        └────────┬─────────┘
                 │
        ┌────────▼──────────────────┐
        │  Retrieved Chunks + Scores│
        └────────┬──────────────────┘
                 │
        ┌────────▼──────────────────┐
        │  Combine Context          │
        └────────┬──────────────────┘
                 │
        ┌────────▼──────────────────┐
        │  LLM Generation           │
        └────────┬──────────────────┘
                 │
        ┌────────▼──────────────────┐
        │  Answer with Sources      │
        └──────────────────────────┘
```

## 📁 Project Structure

```
rag-local/
├── main.py                 # Interactive CLI & RAG pipeline
├── llm.py                  # LLM integration
├── embedder.py             # Text embedding generation
├── docker-compose.yml      # Neo4j container setup
├── data/
│   └── history.txt         # Source document (historical data)
└── retrieval/
    ├── __init__.py
    ├── ingestion.py        # Document processing & storage
    └── vector_search.py    # Semantic search implementation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Docker (for Neo4j)
- Required Python packages (see below)

### Setup

1. **Start Neo4j Database:**
   ```bash
   docker-compose up -d
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the System:**
   ```bash
   python main.py
   ```

## 💬 Usage

Once the system is running, you'll see:
```
📚 Local History RAG System
Type 'exit' to quit.

Ask a question: When did Napoleon invade Russia?
```

The system will:
1. **Retrieve** relevant historical chunks with similarity scores
2. **Display** the context sources
3. **Generate** an answer using the LLM
4. **Show** the final answer

### Example Questions

- When was Napoleon born?
- When did Napoleon invade Russia?
- What happened in 1815 to Napoleon?
- When did World War I begin?
- When did World War II end?
- When did the Cold War end?
- Who invaded Poland in 1939?
- What event triggered World War I?

## 🔧 Core Components

### `main.py`
- Interactive CLI interface
- Loads historical data from `history.txt`
- Implements the RAG pipeline
- Handles user input/output

### `retrieval/ingestion.py`
- Processes raw text into chunks
- Generates embeddings for each chunk
- Stores chunks in Neo4j database

### `retrieval/vector_search.py`
- Performs semantic similarity search
- Returns top-k relevant chunks with scores
- Uses embeddings to find contextually relevant content

### `llm.py`
- Integrates with LLM API
- Generates contextual answers
- Receives retrieved context + question

### `embedder.py`
- Creates vector embeddings from text
- Used by ingestion and vector search

## 📊 Data Flow

1. **Initialization:**
   - `history.txt` is loaded
   - Document is split into chunks
   - Embeddings are generated for each chunk
   - Chunks are stored in Neo4j

2. **Query Time:**
   - User question is embedded
   - Vector search finds similar chunks
   - Context is formatted
   - LLM generates answer based on context

## 🗄️ Database

**Neo4j** stores:
- Document chunks
- Embeddings for semantic search
- Metadata and relationships
- System configuration

Data location: `../data/databases/neo4j/`

## 📝 Configuration

Modify `docker-compose.yml` for Neo4j settings:
- Port: 7687 (default)
- Memory: Adjust based on document size
- Authentication: Configure as needed

## 🐛 Troubleshooting

- **"Connection refused"** → Make sure Neo4j is running (`docker-compose up -d`)
- **"history.txt not found"** → Ensure the file exists in the `data/` directory
- **"Module not found"** → Install dependencies (`pip install -r requirements.txt`)
- **Slow retrieval** → Consider reducing document size or adding indexes

## 🎓 How It Works

1. **Embedding:** Text is converted to vectors using an embedding model
2. **Similarity Search:** Question embedding is compared with chunk embeddings
3. **Ranking:** Results are ranked by similarity score
4. **Context Building:** Top results are combined with metadata
5. **Generation:** LLM uses context to generate grounded answers

## 📚 Resources

- [RAG Concepts](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
- [Neo4j Documentation](https://neo4j.com/docs/)
- [Vector Embeddings](https://en.wikipedia.org/wiki/Word_embedding)

## 📄 License

[Add your license here]

---

**Happy Exploring!** 🚀
