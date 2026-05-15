from ai_agents.agents.research_agent import run_research_agent
from ai_agents.agents.risk_agent import run_risk_agent
from ai_agents.agents.reporting_agent import generate_report

from ai_agents.services.web_search_service import search_web
from ai_agents.services.memory_service import save_interaction, get_memory
from ai_agents.services.llm_market_service import generate_market_analysis
from ai_agents.services.intelligence_layer import build_intelligence


# -----------------------------
# 🚀 MAIN DISTRIBUTION AGENT
# -----------------------------
def run_distribution_agent(query: str, portfolio_id=None, user_id="default"):

    query_lower = (query or "").lower()

    # -----------------------------
    # 🧠 LOAD MEMORY
    # -----------------------------
    history = get_memory(user_id) or []

    # -----------------------------
    # 🎯 INTENT DETECTION
    # -----------------------------
    if any(k in query_lower for k in ["market", "news", "economy", "outlook"]):
        intent = "market"

    elif any(k in query_lower for k in ["risk", "portfolio", "exposure"]):
        intent = "risk"

    elif "report" in query_lower:
        intent = "report"

    else:
        intent = "general"

    # -----------------------------
    # 📊 MARKET FLOW (INTELLIGENCE + LLM)
    # -----------------------------
    if intent == "market":

        research = run_research_agent() or []
        web = search_web(query) or []

        # 🧠 Build intelligence layer
        intel = build_intelligence(research, web)

        print("🔥 FINAL INTEL:", intel)

        # 🤖 LLM reasoning
        response = generate_market_analysis(intel)

        print("FINAL RESPONSE:", response)

    # -----------------------------
    # ⚠️ RISK FLOW
    # -----------------------------
    elif intent == "risk":

        risk = run_risk_agent(portfolio_id) or {}

        response = {
            "type": "risk_summary",
            "risk_score": risk.get("risk_score"),
            "key_risks": risk.get("concentration_risk", [])[:2]
        }

    # -----------------------------
    # 📄 REPORT FLOW
    # -----------------------------
    elif intent == "report":

        report = generate_report(portfolio_id) or {}

        response = {
            "type": "report_summary",
            "summary": report.get("executive_summary"),
            "alerts": report.get("key_alerts", [])[:3]
        }

    # -----------------------------
    # 💬 GENERAL FALLBACK
    # -----------------------------
    else:

        response = {
            "message": "I can help with market insights, portfolio risk, or reports. Please specify your request."
        }

    # -----------------------------
    # 💾 SAVE MEMORY
    # -----------------------------
    save_interaction(user_id, query, response)

    # -----------------------------
    # 📤 FINAL OUTPUT
    # -----------------------------
    return {
        "response": response,
        "history": history[-5:]
    }