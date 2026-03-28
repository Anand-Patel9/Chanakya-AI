const axios = require("axios");

// FastAPI base URL
const FASTAPI_URL = "http://127.0.0.1:8000";

// -----------------------------
// 🔹 Research Agent
// -----------------------------
exports.researchAgent = async (req, res) => {
  try {
    const response = await axios.post(`${FASTAPI_URL}/research`);

    res.json(response.data);
  } catch (error) {
    res.status(500).json({
      error: "Research Agent Failed",
      details: error.message,
    });
  }
};

// -----------------------------
// 🔹 Risk Agent
// -----------------------------
exports.riskAgent = async (req, res) => {
  try {
    const response = await axios.get(`${FASTAPI_URL}/risk`);

    res.json(response.data);
  } catch (error) {
    res.status(500).json({
      error: "Risk Agent Failed",
      details: error.message,
    });
  }
};

// -----------------------------
// 🔹 Communication Agent
// -----------------------------
exports.communicationAgent = async (req, res) => {
  try {
    const { question } = req.body;

    const response = await axios.post(`${FASTAPI_URL}/communication`, {
      question,
    });

    res.json(response.data);
  } catch (error) {
    res.status(500).json({
      error: "Communication Agent Failed",
      details: error.message,
    });
  }
};

// -----------------------------
// 🔹 Portfolio Agent (ML Model)
// -----------------------------
exports.portfolioAgent = async (req, res) => {
  try {
    const response = await axios.get(`${FASTAPI_URL}/portfolio`);

    res.json(response.data);
  } catch (error) {
    res.status(500).json({
      error: "Portfolio Agent Failed",
      details: error.message,
    });
  }
};