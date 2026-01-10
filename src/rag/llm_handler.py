import ollama
from typing import List, Tuple

SYSTEM_PROMPT = (
    "You are a helpful email assistant. Use the following email snippets "
    "to answer the question. If the answer isn't in the snippets, say you "
    "don't know. Always cite the Sender and Date."
)

def build_context(snippets: List[Tuple]):
    lines = []
    for email_id, chunk_id, sender, subject, date, content in snippets:
        # Limit each chunk to 200 chars
        truncated = content[:200] + "..." if len(content) > 200 else content
        lines.append(
            f"[Email {email_id} | {sender} | {date} | {subject}]\n{truncated}"
        )
    return "\n\n".join(lines)



def answer_query(query: str, snippets: List[Tuple]) -> str:
    context = build_context(snippets)
    
    # DEBUG: Check context length
    print(f"[DEBUG] Context length: {len(context)} chars")
    
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Question: {query}\n\n"
        f"Email snippets:\n{context}\n\n"
        "Answer:"
    )
    
    # DEBUG: Check full prompt length
    print(f"[DEBUG] Full prompt length: {len(prompt)} chars")
    
    resp = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return resp["message"]["content"]

