require("dotenv").config();

const app = require("./app");

// Import routes
const agentRoutes = require("./routes/agent.routes");

const PORT = process.env.PORT || 5000;

// Register routes


// Health check
app.get("/", (req, res) => {
  res.send("Node.js Backend Running 🚀");
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});