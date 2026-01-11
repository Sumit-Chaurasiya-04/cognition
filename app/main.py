import sys
import os

# --- PATH FIX: Add the current directory to Python path ---
# This ensures imports work correctly whether running via Streamlit or Pytest
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
from processor import DocumentProcessor
from graph_utils import generate_graph_html
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Cognition AI",
    page_icon="🧠",
    layout="wide"
)

# ... (Rest of the file remains exactly the same) ...

# --- INIT BACKEND ---
@st.cache_resource
def get_processor():
    return DocumentProcessor()

processor = get_processor()

# --- SIDEBAR: CONTROLS ---
st.sidebar.title("🧠 Cognition")
st.sidebar.markdown("---")

st.sidebar.header("1. Add Data")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs, TXT, or CSV", 
    type=["pdf", "txt", "csv", "md"], 
    accept_multiple_files=True
)

if st.sidebar.button("Ingest & Process"):
    if uploaded_files:
        with st.spinner("Reading and embedding documents..."):
            count = 0
            for uploaded_file in uploaded_files:
                success, msg = processor.ingest_document(uploaded_file, uploaded_file.name)
                if success:
                    count += 1
                else:
                    st.error(f"Error: {msg}")
            st.sidebar.success(f"Processed {count} files successfully!")
    else:
        st.sidebar.warning("Please upload files first.")

st.sidebar.markdown("---")
if st.sidebar.button("⚠️ Clear Database"):
    processor.clear_database()
    st.sidebar.success("Database cleared.")

# --- MAIN AREA ---

tab1, tab2, tab3 = st.tabs(["🔎 Semantic Search", "🕸️ Knowledge Graph", "ℹ️ About"])

with tab1:
    st.header("Semantic Search")
    st.markdown("Ask questions or type concepts. The AI matches *meaning*, not just keywords.")
    
    query = st.text_input("Enter your query:", placeholder="e.g., 'Summary of financial results' or 'How to bake a cake'")
    
    if query:
        results = processor.search(query)
        
        # Results come back as a dictionary of lists
        if results and results['documents']:
            num_res = len(results['documents'][0])
            for i in range(num_res):
                doc_text = results['documents'][0][i]
                meta = results['metadatas'][0][i]
                score = results['distances'][0][i]
                
                with st.expander(f"Result {i+1} (Source: {meta['source']})"):
                    st.markdown(f"**Relevance Distance:** {score:.4f}")
                    st.info(doc_text)
        else:
            st.info("No documents found. Upload some data first!")

with tab2:
    st.header("Knowledge Graph")
    st.markdown("Visualize the connections between your uploaded documents.")
    
    if st.button("Generate Graph"):
        data = processor.get_all_documents()
        if data and len(data['ids']) > 0:
            html_path = generate_graph_html(data['documents'], data['metadatas'], data['ids'])
            
            # Read the HTML file and display it
            with open(html_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            components.html(source_code, height=550, scrolling=True)
        else:
            st.warning("Database is empty.")

with tab3:
    st.markdown("""
    ### About Cognition
    **Cognition** is a forward-looking Personal Knowledge Management (PKM) tool.
    
    * **Tech Stack:** Streamlit, ChromaDB, Sentence-Transformers.
    * **Privacy:** All ML runs locally on your CPU.
    * **Roadmap:** Check `docs/roadmap.md` for future plans.
    """)