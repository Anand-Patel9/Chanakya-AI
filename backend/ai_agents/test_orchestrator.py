import os
from dotenv import load_dotenv

# Get path to backend folder (one level up)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH)

# Debug (remove later)
print("GROQ:", os.getenv("GROQ_API_KEY"))