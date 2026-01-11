import os
import pandas as pd
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF
import uuid

# --- CONFIGURATION ---
# We use a persistent local path for the database.
DB_PATH = os.path.join(os.getcwd(), "chroma_db")
COLLECTION_NAME = "cognition_knowledge"

class DocumentProcessor:
    def __init__(self):
        # Initialize the vector database client
        self.client = chromadb.PersistentClient(path=DB_PATH)
        
        # Initialize or get the collection
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)
        
        # Load the AI model. 
        # 'all-MiniLM-L6-v2' is a perfect balance of speed (CPU friendly) and accuracy.
        # It maps sentences to a 384 dimensional dense vector space.
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def read_file(self, file_obj, filename):
        """Reads text from uploaded file objects (PDF, TXT, CSV)."""
        text = ""
        ext = filename.split('.')[-1].lower()
        
        try:
            if ext == 'pdf':
                doc = fitz.open(stream=file_obj.read(), filetype="pdf")
                for page in doc:
                    text += page.get_text()
            elif ext == 'txt':
                text = file_obj.read().decode("utf-8")
            elif ext == 'csv':
                df = pd.read_csv(file_obj)
                # Convert all columns to a single string representation per row
                text = df.to_string(index=False)
            elif ext == 'md':
                text = file_obj.read().decode("utf-8")
        except Exception as e:
            return None, str(e)
            
        return text, None

    def chunk_text(self, text, chunk_size=500):
        """Splits large text into smaller chunks for better embedding accuracy."""
        # Simple character splitting for this version. 
        # Future upgrade: RecursiveCharacterTextSplitter from LangChain.
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    def ingest_document(self, file_obj, filename):
        """Main pipeline: Read -> Chunk -> Embed -> Store."""
        full_text, error = self.read_file(file_obj, filename)
        if error:
            return False, error
        
        chunks = self.chunk_text(full_text)
        if not chunks:
            return False, "File is empty."

        # Generate Embeddings (Vector representations of the text)
        embeddings = self.model.encode(chunks)
        
        # Prepare data for ChromaDB
        ids = [f"{filename}_{str(uuid.uuid4())[:8]}" for _ in chunks]
        metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]
        
        self.collection.add(
            documents=chunks,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
            ids=ids
        )
        return True, f"Successfully processed {len(chunks)} chunks from {filename}."

    def search(self, query, n_results=5):
        """Semantic search: finds text chunks with similar meaning to the query."""
        query_embedding = self.model.encode([query]).tolist()
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        return results

    def get_all_documents(self):
        """Retrieves all documents for visualization."""
        # ChromaDB .get() returns all if no filters provided
        return self.collection.get()
    
    def clear_database(self):
        """Deletes the collection to reset."""
        self.client.delete_collection(COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)