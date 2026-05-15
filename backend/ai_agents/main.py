import os
from dotenv import load_dotenv

# -----------------------------
# ENV LOAD
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)

print("GROQ:", os.getenv("GROQ_API_KEY"))
print("NEWS:", os.getenv("NEWS_API_KEY"))

# -----------------------------
# IMPORTS
# -----------------------------
from fastapi import FastAPI

from ai_agents.api.rag_api import router as rag_router
from ai_agents.routes.research_routes import router as research_router

from ai_agents.agents.risk_agent import run_risk_agent
from ai_agents.agents.compliance_agent import run_compliance_agent
from ai_agents.agents.reporting_agent import generate_report
from ai_agents.agents.distribution_agent import run_distribution_agent
from ai_agents.orchestrator import run_orchestrator   # ✅ FIXED

# -----------------------------
# APP INIT
# -----------------------------
app = FastAPI()

app.include_router(research_router)
app.include_router(rag_router, prefix="/rag")

# -----------------------------
# RISK ONLY
# -----------------------------
@app.get("/risk")
def get_risk(portfolio_id: str = None):
    return run_risk_agent(portfolio_id)

# -----------------------------
# RISK + COMPLIANCE
# -----------------------------
@app.get("/risk-compliance")
def get_risk_compliance(portfolio_id: int = None):

    risk_output = run_risk_agent(portfolio_id)

    compliance_output = run_compliance_agent({
        "risk_output": risk_output
    })

    return {
        "risk": risk_output,
        "compliance": {
            "status": compliance_output["compliance_status"],
            "violations": compliance_output["violations"]
        }
    }

# -----------------------------
# REPORT
# -----------------------------
@app.get("/report")
def get_report(portfolio_id: int = None):
    return generate_report(portfolio_id)

# -----------------------------
# 🔥 MAIN CHAT (NEW SYSTEM)
# -----------------------------
@app.get("/chat")
def chat(query: str):
    try:
        return run_orchestrator(query)
    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# 🧪 LEGACY CHAT (OLD SYSTEM)
# -----------------------------
@app.get("/chat-legacy")
async def chat_legacy(query: str, user_id: str = "default", portfolio_id: int = None):
    try:
        return run_distribution_agent(query, portfolio_id, user_id)
    except Exception as e:
        return {"error": str(e)}