# src/indexing/embedder.py
from typing import List
from langchain_community.embeddings import OllamaEmbeddings
from src.ingestion.parser import EmailDocument

embeddings_model = OllamaEmbeddings(model="mxbai-embed-large")

def embed_documents(docs: List[EmailDocument]) -> List[List[float]]:
    texts = [d.text_content for d in docs]
    return embeddings_model.embed_documents(texts)
