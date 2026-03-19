const axios = require("axios");

exports.runCommunicationAgent = async (req, res) => {

  try {

    const { question } = req.body;

    const response = await axios.post(
      "http://127.0.0.1:8000/communication",
      { question }
    );

    res.json(response.data);

  } catch (error) {

    console.error(error);

    res.status(500).json({ error: "Communication Agent failed" });

  }

};