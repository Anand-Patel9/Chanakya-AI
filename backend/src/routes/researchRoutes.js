const express = require('express');
const router = express.Router();
const axios = require('axios');

// Forward request to FastAPI
router.post('/generate', async (req, res) => {
  try {
    const response = await axios.post(
      'http://127.0.0.1:8000/research/generate',
      req.body
    );
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/insights', async (req, res) => {
  try {
    const response = await axios.get(
      'http://127.0.0.1:8000/research/insights'
    );
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;