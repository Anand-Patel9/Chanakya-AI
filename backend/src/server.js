require("dotenv").config();

const app = require("./app");
const researchRoutes = require("./routes/researchRoutes");

const PORT = process.env.PORT || 5000;

// Register routes FIRST
app.use("/api", researchRoutes);

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});