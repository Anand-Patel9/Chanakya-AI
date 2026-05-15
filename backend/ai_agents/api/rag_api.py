# api/rag_api.py

import os
import uuid
from fastapi import APIRouter, UploadFile, File
from ai_agents.services.document_loader import load_document
from ai_agents.services.vector_store import store_document
from ai_agents.services.rag_service import generate_rag_answer

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -----------------------------
# 📤 Upload Document
# -----------------------------
@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):

    file_ext = file.filename.split(".")[-1].lower()

    doc_id = str(uuid.uuid4())

    file_path = os.path.join(UPLOAD_DIR, f"{doc_id}.{file_ext}")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = load_document(file_path, file_ext)

    chunks = store_document(doc_id, text)

    return {
        "status": "uploaded",
        "doc_id": doc_id,
        "chunks": chunks
    }


# -----------------------------
# 🔎 Query Document
# -----------------------------
@router.post("/ask")
def ask_query(data: dict):

    query = data.get("query")
    doc_id = data.get("doc_id")

    result = generate_rag_answer(query, doc_id)

    return result