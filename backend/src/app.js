const express = require("express");
const cors = require("cors");

const researchRoutes = require("./routes/researchRoutes");
const riskRoutes = require("./routes/riskRoutes");
const communicationRoutes = require("./routes/communicationRoutes");

const app = express();

app.use(cors());
app.use(express.json());

app.use("/api", researchRoutes);
app.use("/api", riskRoutes);
app.use("/api", communicationRoutes);

module.exports = app;