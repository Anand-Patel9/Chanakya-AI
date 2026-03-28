const express = require("express");
const router = express.Router();

const {
  researchAgent,
  riskAgent,
  communicationAgent,
  portfolioAgent,
} = require("../controllers/agent.controller");

// 🔹 Research
router.post("/research", researchAgent);

// 🔹 Risk
router.get("/risk", riskAgent);

// 🔹 Communication
router.post("/communication", communicationAgent);

// 🔹 Portfolio (ML Model)
router.get("/portfolio", portfolioAgent);

module.exports = router;