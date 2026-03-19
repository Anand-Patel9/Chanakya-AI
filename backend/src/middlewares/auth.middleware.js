const jwt = require("jsonwebtoken");
const supabase = require("../services/supabase.service");

const JWT_SECRET = "supersecretkey"; // move to .env later

module.exports = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader) {
      return res.status(401).json({ error: "No token provided" });
    }

    const token = authHeader.split(" ")[1];

    if (!token) {
      return res.status(401).json({ error: "Invalid token format" });
    }

    // Verify JWT
    const decoded = jwt.verify(token, JWT_SECRET);

    // Check if session exists in DB
    const { data: session, error } = await supabase
      .from("sessions")
      .select("*")
      .eq("token", token)
      .single();

    if (error || !session) {
      return res.status(401).json({ error: "Session not found" });
    }

    // Attach user_id to request
    req.user = {
      id: decoded.user_id
    };

    next();

  } catch (err) {
    return res.status(401).json({ error: "Unauthorized" });
  }
};