from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class EmailDocument:
    text_content: str
    metadata: Dict[str, Any]

def email_to_document(email: Dict[str, Any]) -> EmailDocument:
    text_content = email["body"]
    metadata = {
        "sender": email["sender"],
        "subject": email["subject"],
        "date": email["date"],
        "user_id": email["user_id"],
        "id": email["id"],
    }
    return EmailDocument(text_content=text_content, metadata=metadata)

import json
from pathlib import Path

def load_sample_emails(path: str = "C:\\Users\\Mithilesh\\Personal_email_rag\\data\\sample_email.json"):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [email_to_document(e) for e in data]
