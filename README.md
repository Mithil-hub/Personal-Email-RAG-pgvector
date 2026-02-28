# Personal Email RAG System

A local, privacy-preserving **Retrieval-Augmented Generation (RAG)** system for querying personal emails with **strict multi-user isolation**.

Built as a practical exploration of privacy-preserving RAG systems

---

## 🎯 Key Features

* Gmail API ingestion with OAuth
* Semantic search using PostgreSQL + pgvector
* Local LLM inference with Mistral 7B (via Ollama)
* Strict multi-user data isolation using `user_id`
* Automated security and isolation tests
* Fully local, no cloud LLM or embedding APIs

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Vector DB:** PostgreSQL + pgvector
* **LLM:** Mistral 7B (Ollama)
* **Embeddings:** mxbai-embed-large
* **Orchestration:** Docker

---

## 📊 Performance Metrics

* **Retrieval latency:** 0.1–0.2 s (pgvector similarity search)
* **Generation latency:** 15–40 s (Mistral 7B on CPU)
* **First query:** 30–50 s (model load included)
* **Subsequent queries:** 15–25 s
* **Email ingestion (5 emails):** ~60 s (embedding is bottleneck)

> Bottleneck: CPU-based LLM inference. GPU or quantized models reduce latency significantly.

---


## 🧪 Example Result

```
Q: What did I receive about Spring 2026?

A: Your Reduced Course Load request was approved for Spring 2026.
[Cited from Gmail | 2026-01-09]

Retrieval: 0.15s | Generation: 18.3s
```



## 🚀 Quick Start


```powershell
$env:POSTGRES_PASSWORD="your_password_here"

docker run --name pgvector-db \
  -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  -p 5432:5432 \
  -d pgvector/pgvector:pg17

ollama pull mistral
ollama pull mxbai-embed-large

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Run

```bash
python index_emails.py    # Gmail ingestion (user_1)
python index_user2.py     # Synthetic data (user_2)
python test_isolation.py  # Verify isolation
python main.py            # Interactive RAG
```

---

---

## 🔒 Security

* All data tagged with `user_id`
* Mandatory `WHERE user_id = ?` filtering at retrieval
* Cross-user access returns zero results
* Gmail API uses OAuth2 (read-only scope)

---



---

## 📚 Docs

* `demo_script.md` – demo walkthrough
* `architecture.md` – system design
* `evaluation_report.md` – testing & metrics

---

## 👤 Author

**Mithilesh Kothand**
M.S. Computer Science, Arizona State University
[mkothand@asu.edu](mailto:mkothand@asu.edu)
