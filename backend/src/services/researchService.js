const axios = require("axios");

const runResearchAgent = async () => {
  const response = await axios.post("http://127.0.0.1:8000/research");
  return response.data;
};

module.exports = { runResearchAgent };