# System Architecture – Personal Email RAG

## High-Level Overview

The Personal Email RAG System is a local, privacy-preserving Retrieval-Augmented Generation pipeline with **multi-user isolation** enforced at the database layer.

---

## Components

### 1. Data Sources

* **User 1:** Real Gmail emails via Gmail API + OAuth
* **User 2:** Synthetic emails for testing and validation

---

### 2. Ingestion Pipeline

1. Email fetch (Gmail API or synthetic generator)
2. Text chunking (~500 characters)
3. Embedding generation using `mxbai-embed-large`
4. Storage in PostgreSQL + pgvector with `user_id`

---

### 3. Vector Database (PostgreSQL + pgvector)

* Stores: `content`, `embedding`, `user_id`, metadata
* Indexes:

  * B-tree index on `user_id`
  * Vector similarity index for embeddings
* Enforces **hard isolation** via `WHERE user_id = ?` filtering

---

### 4. Retrieval Layer

* User query → embedding
* pgvector similarity search
* Filtered strictly by `user_id`

---

### 5. Generation Layer

* Local LLM: **Mistral 7B** via Ollama
* Retrieved chunks injected into prompt
* Generates grounded, email-specific responses

---

## Security & Isolation

* No shared embeddings across users
* Empty or missing `user_id` is rejected
* Cross-user queries return zero results

---

## Deployment Model

* Fully local (CPU-only)
* Dockerized database
* No external vector or LLM services

---

## Architecture Summary

This architecture prioritizes **privacy**, **security**, and **clarity**, making it suitable for personal assistants and enterprise-style multi-tenant RAG systems.
