# index_emails.py
from src.ingestion.parser import load_sample_emails
from src.indexing.vector_store import chunk_email, init_db, insert_chunks
from src.indexing.embedder import embed_documents
'''
def main():
    init_db()
    docs = load_sample_emails()
    chunked = [c for d in docs for c in chunk_email(d)]
    vectors = embed_documents(chunked)
    insert_chunks(chunked, vectors)
    print("Inserted", len(chunked), "chunks into pgvector")

if __name__ == "__main__":
    main()'''


from src.indexing.vector_store import chunk_email, init_db, insert_chunks
from src.indexing.embedder import embed_documents
from src.ingestion.gmail_client import fetch_latest_emails   # add this import

def main():
    init_db()
    docs = fetch_latest_emails(user_id="mkothand", max_results=5)  # real Gmail
    chunked = [c for d in docs for c in chunk_email(d)]
    vectors = embed_documents(chunked)
    insert_chunks(chunked, vectors)
    print("Inserted", len(chunked), "Gmail chunks into pgvector")

if __name__ == "__main__":
    main()
