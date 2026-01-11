import networkx as nx
from pyvis.network import Network
import tempfile
import os

def generate_graph_html(documents, metadatas, ids):
    """
    Constructs a NetworkX graph from documents and generates an HTML file.
    Nodes = Documents (Source Files) and Concepts (Chunks).
    Edges = Membership (Chunk belongs to File).
    """
    G = nx.Graph()
    
    # 1. Add Source File Nodes (Central Hubs)
    unique_sources = set(m['source'] for m in metadatas)
    for source in unique_sources:
        G.add_node(source, label=source, color='#ff7f0e', title=f"File: {source}", size=25)
    
    # 2. Add Chunk Nodes and connect to Source
    # Limit nodes to prevent UI lag in browser
    max_nodes = 100 
    
    for i, (doc_id, meta, text) in enumerate(zip(ids, metadatas, documents)):
        if i > max_nodes: break
        
        # Create a short label for the chunk
        short_label = text[:20] + "..." if len(text) > 20 else text
        
        G.add_node(doc_id, label=short_label, color='#1f77b4', title=text, size=10)
        G.add_edge(meta['source'], doc_id)

    # 3. Generate PyVis Network
    nt = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="black")
    nt.from_nx(G)
    
    # Physics options for stability
    nt.set_options("""
    var options = {
      "physics": {
        "hierarchicalRepulsion": {
          "nodeDistance": 120
        }
      }
    }
    """)
    
    # Save to a temporary HTML file so Streamlit can render it
    path = os.path.join(tempfile.gettempdir(), "cognition_graph.html")
    nt.save_graph(path)
    return path