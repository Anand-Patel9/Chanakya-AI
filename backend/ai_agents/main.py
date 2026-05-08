import os
from dotenv import load_dotenv

# ✅ LOAD ENV FIRST
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)

print("GROQ:", os.getenv("GROQ_API_KEY"))
print("NEWS:", os.getenv("NEWS_API_KEY"))

# ✅ IMPORTS
from fastapi import FastAPI
from agents.research_agent import run_research_agent
from routes.research_routes import router as research_router
from agents.risk_agent import run_risk_agent
from agents.compliance_agent import run_compliance_agent
from agents.reporting_agent import generate_report
from agents.distribution_agent import run_distribution_agent

app = FastAPI()

app.include_router(research_router)

# -----------------------------
# RISK ONLY
# -----------------------------
@app.get("/risk")
def get_risk(portfolio_id: str = None):
    return run_risk_agent(portfolio_id)

# -----------------------------
# RISK + COMPLIANCE (CORRECT FLOW)
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

@app.get("/report")
def get_report(portfolio_id: int = None):
    return generate_report(portfolio_id)

@app.get("/chat")
async def chat(query: str, user_id: str = "default", portfolio_id: int = None):
    try:
        return run_distribution_agent(query, portfolio_id, user_id)
    except Exception as e:
        return {"error": str(e)}