# Cognition Architecture

## High-Level Overview

Cognition follows a standard "RAG" (Retrieval-Augmented Generation) architecture, stripped down to run entirely locally without the "Generation" part (for now), focusing on Retrieval and Insight.

1.  **Frontend (UI):** Streamlit. Handles user input and displays graphs.
2.  **Orchestrator:** `processor.py`. Manages the flow of data.
3.  **Embeddings Engine:** Sentence-Transformers (`all-MiniLM-L6-v2`). Converts text to vectors.
4.  **Vector Store:** ChromaDB. Stores vectors and performs nearest-neighbor search.
5.  **Graph Engine:** NetworkX + PyVis. Generates visualizations.

## Boundaries & Swappability

* **Model:** The model is initialized in `processor.py`. 
    * *To upgrade:* Change `SentenceTransformer('all-MiniLM-L6-v2')` to any other HuggingFace model string (e.g., `multi-qa-mpnet-base-dot-v1` for higher accuracy but slower speed).
* **Database:** Currently ChromaDB.
    * *To swap:* The `DocumentProcessor` class wraps all DB calls. You could rewrite `ingest_document` and `search` to use FAISS or SQLite with FTS5 without breaking the UI.

## Data Flow
User Upload -> `read_file()` -> `chunk_text()` -> `model.encode()` -> `collection.add()` (ChromaDB).
User Search -> `model.encode()` -> `collection.query()` -> UI Display.