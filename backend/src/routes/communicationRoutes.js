const express = require("express");
const router = express.Router();

const { runCommunicationAgent } = require("../controllers/communicationController");

router.post("/communication", runCommunicationAgent);

module.exports = router;