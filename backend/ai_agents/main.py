from fastapi import FastAPI
from pydantic import BaseModel

from agents.research_agent import run_research_agent
from agents.risk_agent import run_risk_agent
from agents.communication_agent import run_communication_agent

app = FastAPI()

class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {"status": "Chanakya AI System Running"}


@app.post("/research")
def research():
    return run_research_agent()


@app.get("/risk")
def risk():
    return run_risk_agent()


@app.post("/communication")
def communication(data: Question):
    return run_communication_agent(data.question)