from agents.research_agent import run_research_agent
from agents.risk_agent import run_risk_agent
from agents.compliance_agent import run_compliance_agent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_report(portfolio_id=None, research_data=None):

    logger.info("Reporting Agent: Generating portfolio report")

    research = research_data or []
    risk = run_risk_agent(portfolio_id)

    compliance_input = {
        "final_response": risk
    }

    compliance = run_compliance_agent(compliance_input)

    return {
        "executive_summary": generate_executive_summary(risk, compliance),
        "key_alerts": generate_alerts(risk, compliance),
        "market_intelligence": build_market_intelligence(research),
        "risk_dashboard": build_risk_dashboard(risk),
        "portfolio_actions": build_top_actions(risk),
        "compliance_status": build_compliance_section(compliance)
    }


# -----------------------------
# 🧠 EXECUTIVE SUMMARY (HUMAN STYLE)
# -----------------------------
def generate_executive_summary(risk, compliance):

    score = risk.get("risk_score", 0)
    status = compliance.get("compliance_status")

    if status == "Failed":
        return "⚠️ Portfolio is non-compliant and requires immediate corrective action."

    if score > 70:
        return "🚨 High-risk portfolio with significant downside exposure."

    if score > 40:
        return "⚠️ Moderate risk detected. Active monitoring recommended."

    return "✅ Portfolio is stable with controlled risk exposure."


# -----------------------------
# 🚨 ALERT ENGINE
# -----------------------------
def generate_alerts(risk, compliance):

    alerts = []

    # High concentration
    for c in risk.get("concentration_risk", []):
        if c.get("risk") == "High":
            alerts.append(f"High concentration in {c.get('sector')}")

    # Compliance issues
    if compliance.get("compliance_status") == "Failed":
        for v in compliance.get("violations", []):
            alerts.append(f"Compliance Issue: {v}")

    # High market risk sectors
    for item in risk.get("portfolio_risk_breakdown", []):
        if item.get("market_risk") == "High":
            alerts.append(f"High market risk in {item.get('sector')}")

    return list(set(alerts))


# -----------------------------
# 📊 MARKET INTELLIGENCE
# -----------------------------
def build_market_intelligence(research):

    top = []

    for r in research[:5]:
        top.append({
            "headline": r.get("title"),
            "sentiment": r.get("sentiment"),
            "recommended_action": r.get("action")
        })

    return top


# -----------------------------
# 📉 RISK DASHBOARD
# -----------------------------
def build_risk_dashboard(risk):

    return {
        "portfolio_value": risk.get("portfolio_value"),
        "risk_score": risk.get("risk_score"),
        "volatility": risk.get("volatility"),
        "value_at_risk": risk.get("value_at_risk"),
        "sector_exposure": risk.get("sector_exposure")
    }


# -----------------------------
# 🎯 TOP ACTIONS (FILTERED)
# -----------------------------
def build_top_actions(risk):

    actions = risk.get("decisions", [])

    # Prioritize important actions only
    priority = []

    for a in actions:
        if a["action"] in ["SELL", "REDUCE"]:
            priority.append(a)

    return priority[:5]


# -----------------------------
# ⚖️ COMPLIANCE
# -----------------------------
def build_compliance_section(compliance):

    return {
        "status": compliance.get("compliance_status"),
        "violations": compliance.get("violations", [])
    }