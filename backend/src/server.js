require("dotenv").config();

const app = require("./app");

// Import routes
const agentRoutes = require("./routes/agent.routes");

const PORT = process.env.PORT || 5000;

// Register routes
app.use("/api", agentRoutes);

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});