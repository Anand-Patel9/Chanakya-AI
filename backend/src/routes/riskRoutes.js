const express = require("express");
const router = express.Router();
const axios = require("axios");

router.get("/risk", async (req, res) => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/risk");
    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.get("/risk-compliance", async (req, res) => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/risk-compliance");
    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;