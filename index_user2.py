# index_user2.py
from src.indexing.vector_store import chunk_email, init_db, insert_chunks
from src.indexing.embedder import embed_documents
from src.ingestion.parser import EmailDocument

def main():
    init_db()
    
    # Synthetic emails for user_2 (different content from user_1)
    user2_emails = [
        EmailDocument(
            text_content="Team meeting scheduled for Monday at 10am in Conference Room B. Please review the Q1 roadmap before attending.",
            metadata={
                "id": "user2_email1",
                "sender": "manager@techcorp.com",
                "subject": "Monday Team Meeting",
                "date": "2026-01-08",
                "user_id": "user_2",
            }
        ),
        EmailDocument(
            text_content="Your performance review is due next week. Please submit your self-assessment by Friday EOD.",
            metadata={
                "id": "user2_email2",
                "sender": "hr@techcorp.com",
                "subject": "Q1 Performance Review",
                "date": "2026-01-07",
                "user_id": "user_2",
            }
        ),
        EmailDocument(
            text_content="Congratulations! Your proposal for the new API integration project has been approved. Budget: $50k.",
            metadata={
                "id": "user2_email3",
                "sender": "cto@techcorp.com",
                "subject": "API Project Approved",
                "date": "2026-01-06",
                "user_id": "user_2",
            }
        ),
    ]
    
    print(f"Indexing {len(user2_emails)} emails for user_2...")
    chunked = [c for d in user2_emails for c in chunk_email(d)]
    print(f"Created {len(chunked)} chunks")
    
    vectors = embed_documents(chunked)
    print(f"Generated {len(vectors)} embeddings")
    
    insert_chunks(chunked, vectors)
    print(f"✅ Inserted {len(chunked)} chunks for user_2 into pgvector")

if __name__ == "__main__":
    main()
