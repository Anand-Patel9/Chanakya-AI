const axios = require("axios");

const runRiskAgent = async (req, res) => {
  try {

    const response = await axios.post("http://127.0.0.1:8000/risk");

    res.json(response.data);

  } catch (error) {

    console.error("Risk Agent Error:", error.message);

    res.status(500).json({
      error: "Risk agent failed"
    });

  }
};

module.exports = { runRiskAgent };