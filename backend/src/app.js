const express = require("express");
const cors = require("cors");

const researchRoutes = require("./routes/researchRoutes");
const riskRoutes = require("./routes/riskRoutes");
const communicationRoutes = require("./routes/communicationRoutes");
const agentRoutes = require("./routes/agent.routes");

const app = express();

app.use(cors());
app.use(express.json());

// Existing routes
app.use("/api", researchRoutes);
app.use("/api", riskRoutes);
app.use("/api", communicationRoutes);

app.use("/api", agentRoutes);

module.exports = app;