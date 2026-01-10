# src/rag/pipeline.py
from typing import List
from langchain_community.embeddings import OllamaEmbeddings
from src.indexing.vector_store import similarity_search

query_embedder = OllamaEmbeddings(model="mxbai-embed-large")

def retrieve_relevant_chunks(query: str, user_id: str, k: int = 5):
    """
    Retrieve email chunks for a specific user with enforced isolation.
    
    Args:
        query: Natural language question
        user_id: REQUIRED. User identifier for data isolation
        k: Number of results to return
    
    Returns:
        List of tuples: (email_id, chunk_id, sender, subject, date, content)
    
    Raises:
        ValueError: If user_id is None, empty, or invalid
    """
    # SECURITY: Enforce user_id validation
    if not user_id or not isinstance(user_id, str) or user_id.strip() == "":
        raise ValueError("user_id is required and cannot be empty")
    
    # Embed the query
    q_emb = query_embedder.embed_query(query)
    print(f"[DEBUG] Query embedding length: {len(q_emb)}")
    
    # SECURITY: Pass user_id to enforce filtering at DB level
    rows = similarity_search(q_emb, user_id=user_id.strip(), k=k)
    print(f"[DEBUG] Retrieved {len(rows)} rows from DB for user_id={user_id}")
    
    return rows
