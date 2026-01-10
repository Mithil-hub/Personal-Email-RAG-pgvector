# Personal Email RAG System – Demo Script

**Project:** Personal Email RAG with Multi-User Support  
**Author:** Mithilesh Kothand  
**Date:** January 2026

---

## Overview

This demo script provides step-by-step instructions to set up, run, and evaluate the **Personal Email RAG System** with **multi-user support**. It demonstrates end-to-end Retrieval-Augmented Generation (RAG), Gmail integration, and strict data isolation between users.

---

## Prerequisites

* Docker Desktop (running)
* Ollama ([https://ollama.ai](https://ollama.ai))
* Python 3.10+ with `venv`
* Gmail API credentials (`credentials.json`)
* Windows OS (PowerShell commands)

---

## Environment Setup

```bash
docker run --name pgvector-db -e POSTGRES_PASSWORD=password -p 5432:5432 -d pgvector/pgvector:pg17
ollama pull mistral
ollama pull mxbai-embed-large
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Data Ingestion

```bash
python index_emails.py   # user_1 (Gmail)
python index_user2.py    # user_2 (synthetic)
```

Verify:

```bash
docker exec -it pgvector-db psql -U postgres -d postgres -c "SELECT user_id, COUNT(*) FROM email_chunks GROUP BY user_id;"
```

---

## Isolation Testing

```bash
python test_isolation.py
```

All tests must pass.

---

## Interactive Queries

```bash
python main.py
```

Query as `user_1` or `user_2` to verify isolated retrieval.

---

## Cleanup

```bash
docker stop pgvector-db
docker rm pgvector-db
```
