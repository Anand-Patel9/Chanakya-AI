import express from "express";
import fetch from "node-fetch";

const router = express.Router();

router.post("/generate", async (req, res) => {
  try {
    const response = await fetch("http://localhost:8000/research/generate", {
      method: "POST"
    });

    const data = await response.json();
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: "Research Agent failed" });
  }
});

router.get("/insights", async (req, res) => {
  const response = await fetch("http://localhost:8000/research/insights");
  const data = await response.json();
  res.json(data);
});

export default router;