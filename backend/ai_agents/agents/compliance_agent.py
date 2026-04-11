from services.compliance_service import check_compliance
from db.supabase_client import store_compliance_log


def run_compliance_agent(state):

    print("Running Compliance Agent...")

    response = state.get("final_response", "")

    # ✅ FIX: ensure string
    if isinstance(response, dict):
        response = str(response)

    result = check_compliance(response)

    store_compliance_log(result)

    return {
        **state,
        "compliance_status": result["status"],
        "violations": result["violations"]
    }