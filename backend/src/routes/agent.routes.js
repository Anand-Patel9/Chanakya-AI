const express = require("express");
const axios = require("axios");

const router = express.Router();

const {
  researchAgent,
  riskAgent,
  communicationAgent,
  portfolioAgent,
} = require("../controllers/agent.controller");

// ------------------------------
// 🔹 EXISTING ROUTES (KEEP)
// ------------------------------

// Research
router.post("/research", researchAgent);

// Risk
router.get("/risk", riskAgent);

// Communication
router.post("/communication", communicationAgent);

// Portfolio
router.get("/portfolio", portfolioAgent);


// ------------------------------
// 🔥 MAIN AI ORCHESTRATOR ROUTE
// ------------------------------
router.post("/ask-ai", async (req, res) => {
  try {
    const { question } = req.body;

    // ✅ Validation
    if (!question) {
      return res.status(400).json({
        error: "Question is required"
      });
    }

    // 🔥 Call FastAPI Orchestrator
    const response = await axios.post(
      "http://127.0.0.1:8000/orchestrate",
      { question }
    );

    // ✅ Send response back to frontend
    res.json(response.data);

  } catch (error) {
    // 🔥 FULL DEBUG (VERY IMPORTANT)
    console.error("❌ FULL ERROR:", error.response?.data || error.message);

    res.status(500).json({
      error: "AI service failed",
      details: error.response?.data || error.message
    });
  }
});

module.exports = router;

console.log("Agent routes loaded successfully");