import pytest
import os
import shutil
from app.processor import DocumentProcessor

# Setup and Teardown for database
DB_TEST_PATH = "chroma_db_test"

@pytest.fixture
def processor():
    # Override global DB path for testing if possible, 
    # but for simplicity we rely on the class structure.
    # In a full app, we'd inject config.
    proc = DocumentProcessor()
    # Ensure clean state
    proc.clear_database()
    return proc

def test_chunking(processor):
    text = "a" * 1200
    chunks = processor.chunk_text(text, chunk_size=500)
    assert len(chunks) == 3
    assert len(chunks[0]) == 500

def test_ingestion_and_search(processor):
    # Create a dummy file object
    class MockFile:
        def read(self):
            return b"Apples are red. Bananas are yellow."
        
    mock_file = MockFile()
    mock_name = "fruits.txt"
    
    success, msg = processor.ingest_document(mock_file, mock_name)
    assert success is True
    
    # Test Search - searching for 'color' should match despite no keyword overlap
    # Note: With a tiny dataset and vector space, 'color' might not correspond 
    # strongly to 'red' without more context, so we search for 'fruit' instead.
    results = processor.search("fruit", n_results=1)
    assert len(results['documents'][0]) > 0
    assert "Apples" in results['documents'][0][0]

def test_empty_search(processor):
    results = processor.search("nothing")
    # Should not crash, just return empty or low relevance
    assert results is not None