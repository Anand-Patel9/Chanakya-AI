const axios = require("axios");

const runResearchAgent = async (req, res) => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/research");
    res.json(response.data);
  } catch (error) {
    console.error("Research Agent Error:", error.message);

    res.status(500).json({
      error: "Failed to fetch research agent data"
    });
  }
};

module.exports = {
  runResearchAgent
};