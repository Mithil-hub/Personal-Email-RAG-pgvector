from __future__ import annotations
from typing import List
import base64
from email.message import EmailMessage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from src.ingestion.parser import EmailDocument
from email.utils import parsedate_to_datetime

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    service = build("gmail", "v1", credentials=creds)
    return service

def list_messages(service, max_results: int = 50):
    resp = service.users().messages().list(userId="me", maxResults=max_results).execute()
    return resp.get("messages", [])

def get_message(service, msg_id: str):
    return service.users().messages().get(userId="me", id=msg_id, format="full").execute()

def parse_message(msg, user_id: str) -> EmailDocument:
    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
    sender = headers.get("From", "")
    subject = headers.get("Subject", "")
    date_str = headers.get("Date", "")
    
    # Parse RFC 2822 date to datetime
    try:
        date = parsedate_to_datetime(date_str)
    except:
        date = None  # fallback if parsing fails
    
    body = ""
    if "parts" in msg["payload"]:
        for part in msg["payload"]["parts"]:
            if part.get("mimeType") == "text/plain" and "data" in part.get("body", {}):
                body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
                break
    elif "data" in msg["payload"].get("body", {}):
        body = base64.urlsafe_b64decode(msg["payload"]["body"]["data"]).decode("utf-8", errors="ignore")

    metadata = {
        "id": msg["id"],
        "sender": sender,
        "recipient": headers.get("To", ""),
        "subject": subject,
        "date": date,  # now a datetime object or None
        "user_id": user_id,
    }
    return EmailDocument(text_content=body, metadata=metadata)


def fetch_latest_emails(user_id: str, max_results: int = 50) -> List[EmailDocument]:
    service = get_gmail_service()
    msgs = list_messages(service, max_results=max_results)
    docs = []
    for m in msgs:
        full = get_message(service, m["id"])
        docs.append(parse_message(full, user_id=user_id))
    return docs
