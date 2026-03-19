const express = require("express");
const router = express.Router();

const { runResearchAgent } = require("../controllers/researchController");

router.get("/research", runResearchAgent);

module.exports = router;