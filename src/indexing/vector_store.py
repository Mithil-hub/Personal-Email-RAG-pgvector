import psycopg2
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.ingestion.parser import EmailDocument




# src/indexing/vector_store.py
import psycopg2
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.ingestion.parser import EmailDocument


DB_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": "password",  # from docker inspect
}

def get_conn():
    return psycopg2.connect(**DB_PARAMS)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS email_chunks (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL,
            email_id TEXT,
            chunk_id INTEGER,
            sender TEXT,
            subject TEXT,
            date TIMESTAMP,
            content TEXT,
            embedding vector(1024)
        );
        """
    )
    # Add index for fast user_id filtering
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_user_id ON email_chunks(user_id);"
    )
    conn.commit()
    cur.close()
    conn.close()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=100,
)

def chunk_email(doc: EmailDocument) -> List[EmailDocument]:
    chunks = text_splitter.split_text(doc.text_content)
    return [
        EmailDocument(
            text_content=chunk,
            metadata={**doc.metadata, "chunk_id": i},
        )
        for i, chunk in enumerate(chunks)
    ]

def insert_chunks(docs: List[EmailDocument], vectors: List[List[float]]):
    conn = get_conn()
    cur = conn.cursor()
    for doc, emb in zip(docs, vectors):
        cur.execute(
            """
            INSERT INTO email_chunks
            (user_id, email_id, chunk_id, sender, subject, date, content, embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                doc.metadata["user_id"],
                doc.metadata.get("id"),
                doc.metadata.get("chunk_id", 0),
                doc.metadata.get("sender"),
                doc.metadata.get("subject"),
                doc.metadata.get("date"),
                doc.text_content,
                emb,
            ),
        )
    conn.commit()
    cur.close()
    conn.close()




def similarity_search(query_embedding, user_id: str, k: int = 5):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT email_id, chunk_id, sender, subject, date, content
        FROM email_chunks
        WHERE user_id = %s  -- ✅ HARD FILTER on user_id
        ORDER BY embedding <-> %s::vector
        LIMIT %s;
        """,
        (user_id, query_embedding, k),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
