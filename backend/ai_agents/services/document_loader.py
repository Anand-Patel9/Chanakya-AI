# services/document_loader.py

import fitz  # PyMuPDF
import pandas as pd
from docx import Document


def load_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text


def load_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])


def load_excel(file_path):
    df = pd.read_excel(file_path)
    return df.astype(str).to_string()


def load_document(file_path, file_type):

    if file_type == "pdf":
        return load_pdf(file_path)

    elif file_type == "docx":
        return load_docx(file_path)

    elif file_type == "xlsx":
        return load_excel(file_path)

    else:
        raise ValueError("Unsupported file type")