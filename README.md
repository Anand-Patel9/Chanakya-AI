## Base URL
http://localhost:3000 (Node)

## Endpoints

### 1. Chat (Main AI)
POST /api/ai/chat

Body:
{
  "query": "Why is market falling?"
}

### 2. Upload Document
POST /api/ai/rag/upload

Form-data:
file: <file>

### 3. Ask Document
POST /api/ai/rag/query

Body:
{
  "query": "Summarize this",
  "doc_id": "..."
}
