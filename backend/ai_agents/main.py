from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import os
import sys

# -------------------------------
# EXISTING AGENTS (KEEP SAME)
# -------------------------------
from agents.research_agent import run_research_agent
from agents.risk_agent import run_risk_agent
from agents.communication_agent import run_communication_agent

# -------------------------------
# 🔥 ADD DATASET PATH (IMPORTANT)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "../Dataset")

sys.path.append(DATASET_PATH)

# -------------------------------
# IMPORT TRAINING COMPONENTS
# -------------------------------
from train_agent import (
    ChanakyaPortfolioEnv,
    pivot_returns,
    top_stocks
)

# -------------------------------
# LOAD MODEL
# -------------------------------
from stable_baselines3 import PPO

MODEL_PATH = os.path.join(DATASET_PATH, "chanakya_portfolio_ppo_final")

model = PPO.load(MODEL_PATH)

# -------------------------------
# FASTAPI INIT
# -------------------------------
app = FastAPI()


class Question(BaseModel):
    question: str


# -------------------------------
# BASIC ROUTES
# -------------------------------
@app.get("/")
def home():
    return {"status": "Chanakya AI System Running 🚀"}


@app.post("/research")
def research():
    return run_research_agent()


@app.get("/risk")
def risk():
    return run_risk_agent()


@app.post("/communication")
def communication(data: Question):
    return run_communication_agent(data.question)


# -------------------------------
# 🔥 NEW: PORTFOLIO ENDPOINT
# -------------------------------
@app.get("/portfolio")
def get_portfolio():

    env = ChanakyaPortfolioEnv(pivot_returns)

    obs, _ = env.reset()

    action, _ = model.predict(obs, deterministic=True)

    # Softmax allocation
    exp_weights = np.exp(action)
    weights = exp_weights / np.sum(exp_weights)

    return {
        "portfolio": dict(zip(top_stocks, weights.tolist()))
    }