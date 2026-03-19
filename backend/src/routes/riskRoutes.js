const express = require("express");
const router = express.Router();

const { runRiskAgent } = require("../controllers/riskController");

router.get("/risk", runRiskAgent);

module.exports = router;