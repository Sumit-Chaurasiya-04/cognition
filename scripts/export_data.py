import sys
import os
# Add parent dir to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.processor import DocumentProcessor
import pandas as pd

def main():
    print("Initializing Processor...")
    proc = DocumentProcessor()
    
    print("Fetching all data...")
    data = proc.get_all_documents()
    
    if not data or len(data['ids']) == 0:
        print("No data found in database.")
        return

    # Flatten the structure for CSV
    ids = data['ids']
    embeddings = data['embeddings'] # List of lists
    documents = data['documents']
    metadatas = data['metadatas']
    
    export_list = []
    for i, doc_id in enumerate(ids):
        row = {
            "ID": doc_id,
            "Content": documents[i],
            "Source": metadatas[i].get('source', 'Unknown'),
            # Convert embedding list to string for single cell storage
            "Embedding_Vector": str(embeddings[i]) 
        }
        export_list.append(row)
        
    df = pd.DataFrame(export_list)
    output_file = "cognition_export.xlsx"
    df.to_excel(output_file, index=False)
    print(f"✅ Exported {len(df)} rows to {output_file}")

if __name__ == "__main__":
    main()