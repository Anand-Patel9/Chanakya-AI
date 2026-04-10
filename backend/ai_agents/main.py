# -------------------------------
# LOAD ENV VARIABLES (VERY FIRST)
# -------------------------------
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH)

# Debug (remove later if needed)
print("GROQ:", os.getenv("GROQ_API_KEY"))


# -------------------------------
# IMPORTS (AFTER ENV LOAD)
# -------------------------------
from fastapi import FastAPI
from pydantic import BaseModel

from agents.risk_agent import run_risk_agent
from agents.research_agent import run_research_agent
from agents.communication_agent import run_communication_agent
from orchestrator import run_orchestrator


# -------------------------------
# FASTAPI INIT
# -------------------------------
app = FastAPI()


# -------------------------------
# REQUEST MODEL
# -------------------------------
class Question(BaseModel):
    question: str


# -------------------------------
# ROOT
# -------------------------------
@app.get("/")
def home():
    return {
        "status": "Chanakya AI System Running 🚀"
    }


# -------------------------------
# RISK AGENT
# -------------------------------
@app.get("/risk")
def risk():
    return run_risk_agent()


# -------------------------------
# RESEARCH AGENT
# -------------------------------
@app.get("/research")
def research():
    return run_research_agent()


# -------------------------------
# COMMUNICATION AGENT
# -------------------------------
@app.post("/communication")
def communication(data: Question):
    return run_communication_agent(data.question)


# -------------------------------
# ORCHESTRATOR (MAIN API)
# -------------------------------
@app.post("/orchestrate")
def orchestrate(data: Question):
    return run_orchestrator(data.question)