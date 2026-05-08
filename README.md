# 🚀 AI Market Intelligence Backend

This backend powers an AI-driven financial intelligence system with:

- 📊 Market Analysis (LLM-based)
- 🧠 Intelligence Layer (macro + drivers)
- 📄 RAG (Document Q&A)
- 📈 Market Impact Engine
- ⚠️ Risk Analysis

---

## 🔹 Base URL

http://localhost:3000/api/ai

---

## 🧠 1. Chat API (Main AI)

### Endpoint
POST /chat

### Request Body
```json
{
  "query": "Why is market falling?"
}

fetch("http://localhost:3000/api/ai/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    query: "Why is market falling?"
  })
})
.then(res => res.json())
.then(data => console.log(data));

POST /rag/upload
file: <upload file>
const formData = new FormData();
formData.append("file", file);

fetch("http://localhost:3000/api/ai/rag/upload", {
  method: "POST",
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));

POST /rag/query

fetch("http://localhost:3000/api/ai/rag/query", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    query: "Summarize this",
    doc_id: "your_doc_id"
  })
})
.then(res => res.json())
.then(data => console.log(data));
