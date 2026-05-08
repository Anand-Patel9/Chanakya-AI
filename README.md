# 🚀 AI Market Intelligence Backend

This backend provides AI-driven financial insights using:

- Market analysis (LLM-based reasoning)
- Intelligence layer (macro + drivers)
- Market impact engine
- Risk analysis
- Document-based Q&A (RAG)

---

## 🔹 Base URL

http://localhost:3000/api/ai

---

## 🔹 How to Use APIs

### 🧠 AI Chat (Main Feature)

Send a query to get market analysis, impact, and risk.

```javascript
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
