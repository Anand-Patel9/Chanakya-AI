const axios = require("axios");

const FASTAPI_URL = "http://127.0.0.1:8000";

// -----------------------------
// 🔥 MAIN AI CHAT (ORCHESTRATOR)
// -----------------------------
exports.chatAI = async (req, res) => {
  try {
    const { query } = req.body;

    if (!query) {
      return res.status(400).json({
        error: "Query is required",
      });
    }

    const response = await axios.get(`${FASTAPI_URL}/chat`, {
      params: { query }
    });

    res.json(response.data);

  } catch (error) {
    console.error("❌ AI ERROR:", error.response?.data || error.message);

    res.status(500).json({
      error: "AI system failed",
      details: error.response?.data || error.message,
    });
  }
};

// -----------------------------
// 🔥 RAG QUERY
// -----------------------------
exports.ragQuery = async (req, res) => {
  try {
    const { query } = req.body;

    const response = await axios.post(
      `${FASTAPI_URL}/rag/query`,
      { query }
    );

    res.json(response.data);

  } catch (error) {
    res.status(500).json({
      error: "RAG query failed",
      details: error.message,
    });
  }
};

// -----------------------------
// 🔥 RAG UPLOAD
// -----------------------------
exports.ragUpload = async (req, res) => {
  try {
    const formData = new FormData();
    formData.append("file", req.file.buffer, req.file.originalname);

    const response = await axios.post(
      `${FASTAPI_URL}/rag/upload`,
      formData,
      {
        headers: formData.getHeaders(),
      }
    );

    res.json(response.data);

  } catch (error) {
    res.status(500).json({
      error: "Upload failed",
      details: error.message,
    });
  }
};