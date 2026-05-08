# services/rag_service.py

import os
from groq import Groq
from services.vector_store import query_document

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_rag_answer(query, doc_id):

    chunks = query_document(doc_id, query)

    if not chunks:
        return {
            "answer": "No relevant data found in document.",
            "sources": []
        }

    context = "\n".join(chunks)

    prompt = f"""
You are a financial analyst.

Use ONLY the context below to answer.

CONTEXT:
{context}

QUESTION:
{query}

RULES:
- Do not hallucinate
- Answer only from context
- Be concise

OUTPUT:
Answer + key points
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": chunks
    }