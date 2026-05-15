from ai_agents.services.compliance_service import check_compliance
from ai_agents.db.supabase_client import store_compliance_log 


def run_compliance_agent(state):

    print("Running Compliance Agent...")

    # 🔥 CHANGE: pass FULL RISK OUTPUT (not just text)
    risk_data = state.get("risk_output", {})

    result = check_compliance(risk_data)

    store_compliance_log(result)

    return {
        **state,
        "compliance_status": result["status"],
        "violations": result["violations"]
    }