from fastapi import FastAPI
from pydantic import BaseModel

# -------------------------------
# IMPORT AGENTS
# -------------------------------
from agents.research_agent import run_research_agent
from agents.risk_agent import run_risk_agent
from agents.communication_agent import run_communication_agent
from agents.portfolio_agent import run_portfolio_agent

# -------------------------------
# FASTAPI INIT
# -------------------------------
app = FastAPI()


class Question(BaseModel):
    question: str


# -------------------------------
# ROOT
# -------------------------------
@app.get("/")
def home():
    return {"status": "Chanakya AI System Running 🚀"}


# -------------------------------
# RESEARCH
# -------------------------------
@app.post("/research")
def research():
    return run_research_agent()


# -------------------------------
# RISK
# -------------------------------
@app.get("/risk")
def risk():
    return run_risk_agent()


# -------------------------------
# COMMUNICATION
# -------------------------------
@app.post("/communication")
def communication(data: Question):
    return run_communication_agent(data.question)


# -------------------------------
# ✅ ONLY PORTFOLIO ROUTE
# -------------------------------
@app.get("/portfolio")
def portfolio():
    return run_portfolio_agent()