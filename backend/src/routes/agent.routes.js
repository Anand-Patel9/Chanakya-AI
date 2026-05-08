const express = require("express");
const multer = require("multer");

const router = express.Router();
const upload = multer();

const {
  chatAI,
  ragQuery,
  ragUpload,
} = require("../controllers/agent.controller");

// ------------------------------
// 🔥 AI ORCHESTRATOR
// ------------------------------
router.post("/chat", chatAI);

// ------------------------------
// 🔥 RAG QUERY
// ------------------------------
router.post("/rag/query", ragQuery);

// ------------------------------
// 🔥 RAG FILE UPLOAD
// ------------------------------
router.post("/rag/upload", upload.single("file"), ragUpload);

module.exports = router;