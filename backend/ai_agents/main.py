import os
from dotenv import load_dotenv

# ✅ LOAD ENV FIRST (BEFORE IMPORTS)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)

print("GROQ:", os.getenv("GROQ_API_KEY"))
print("NEWS:", os.getenv("NEWS_API_KEY"))

# ✅ NOW IMPORT
from agents.research_agent import run_research_agent
from routes.research_routes import router as research_router
from agents.risk_agent import run_risk_agent
from fastapi import FastAPI

app = FastAPI()

app.include_router(research_router)

@app.get("/risk")
def get_risk(portfolio_id: int = None):
    return run_risk_agent(portfolio_id)