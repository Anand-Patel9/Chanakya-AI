from langgraph.graph import StateGraph
from typing import TypedDict, Dict, Any

from agents.research_agent import run_research_agent
from agents.risk_agent import run_risk_agent

# -----------------------------
# 🧠 STATE DEFINITION
# -----------------------------
class AgentState(TypedDict, total=False):
    query: str

    research_data: Any
    risk_data: Dict

    intelligence: Dict
    analysis: Dict
    impact: Dict

    route: str
    final_response: Dict

    compliance_status: str
    violations: list

    rag_context: str
    doc_id: str  


# -----------------------------
# 🔀 ROUTER
# -----------------------------
def route_query(state: AgentState):

    query = (state.get("query") or "").lower()

    portfolio_keywords = [
        "portfolio", "holdings", "allocation", "investments"
    ]

    if any(k in query for k in portfolio_keywords):
        return "portfolio_flow"

    return "market_flow"


def router_node(state: AgentState):

    decision = route_query(state)

    print(f"🔀 Routing decision: {decision}")

    return {**state, "route": decision}


# -----------------------------
# 🔍 RESEARCH NODE
# -----------------------------
def research_node(state: AgentState):

    print("🚀 Running Research Agent...")

    try:
        result = run_research_agent(state.get("query", ""))
    except Exception as e:
        print("❌ Research error:", e)
        result = []

    return {**state, "research_data": result}


# -----------------------------
# 🧠 INTELLIGENCE NODE
# -----------------------------
def intelligence_node(state: AgentState):

    print("🧠 Running Intelligence Layer...")

    try:
        from services.intelligence_layer import build_intelligence

        intel = build_intelligence(
            state.get("research_data", []) or [],
            []  # web optional (you can plug later)
        )

    except Exception as e:
        print("❌ Intelligence error:", e)
        intel = {"macro": [], "drivers": []}

    return {**state, "intelligence": intel}


# -----------------------------
# 🤖 ANALYSIS NODE (LLM)
# -----------------------------
def analysis_node(state: AgentState):

    print("🤖 Running Market Analysis (LLM)...")

    try:
        from services.llm_market_service import generate_market_analysis

        analysis = generate_market_analysis({
            **state.get("intelligence", {}),
            "rag": state.get("rag_context", "")
        })

    except Exception as e:
        print("❌ Analysis error:", e)
        analysis = {
            "type": "market_update",
            "what_is_happening": "Analysis failed.",
            "why_it_is_happening": "System error.",
            "what_to_do": "Retry request."
        }

    return {**state, "analysis": analysis}


# -----------------------------
# 📊 IMPACT NODE
# -----------------------------
def impact_node(state: AgentState):

    print("📊 Running Market Impact Engine...")

    try:
        from services.market_impact_engine import build_market_impact

        impact = build_market_impact(
            state.get("intelligence", {}) or {}
        )

    except Exception as e:
        print("❌ Impact error:", e)
        impact = {}

    return {**state, "impact": impact}


# -----------------------------
# ⚠️ RISK NODE
# -----------------------------
def risk_node(state: AgentState):

    print("⚠️ Running Risk Agent...")

    try:
        risk = run_risk_agent()
    except Exception as e:
        print("❌ Risk error:", e)
        risk = {}

    return {**state, "risk_data": risk}


# -----------------------------
# 💬 COMMUNICATION NODE
# -----------------------------
def communication_node(state: AgentState):

    print("💬 Building Final Response...")

    try:
        response = {
            "analysis": state.get("analysis"),
            "impact": state.get("impact"),
            "risk": state.get("risk_data")
        }
    except Exception as e:
        response = {"error": str(e)}

    print("✅ FINAL RESPONSE:", response)

    return {**state, "final_response": response}


# -----------------------------
# 🛡️ COMPLIANCE NODE
# -----------------------------
def compliance_node(state: AgentState):

    print("🛡️ Running Compliance Agent...")

    try:
        from agents.compliance_agent import run_compliance_agent

        return run_compliance_agent(state)

    except Exception as e:
        print("❌ Compliance error:", e)

        return {
            **state,
            "compliance_status": "error",
            "violations": [str(e)]
        }
    
# -----------------------------
#  📚 RAG NODE
# -----------------------------
def rag_node(state: AgentState):

    print("📚 Running RAG Retrieval...")

    try:
        from services.rag_service import generate_rag_answer

        doc_id = state.get("doc_id")  # optional

        if not doc_id:
            return {**state, "rag_context": ""}

        rag_result = generate_rag_answer(
            state.get("query"),
            doc_id
        )

        context = rag_result.get("answer", "")

        return {**state, "rag_context": context}

    except Exception as e:
        print("❌ RAG error:", e)
        rag_result = ""

    return {**state, "rag_context": rag_result}


# -----------------------------
# 🧩 GRAPH BUILDER
# -----------------------------
def build_graph():

    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("router", router_node)
    graph.add_node("research", research_node)
    graph.add_node("intelligence", intelligence_node)
    graph.add_node("analysis", analysis_node)
    graph.add_node("impact", impact_node)
    graph.add_node("risk", risk_node)
    graph.add_node("communication", communication_node)
    graph.add_node("compliance", compliance_node)

    # Start
    graph.add_edge("__start__", "router")

    # Routing
    graph.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {
            "market_flow": "research",
            "portfolio_flow": "risk"
        }
    )

    # MARKET FLOW
    graph.add_edge("research", "intelligence")
    graph.add_edge("intelligence", "analysis")
    graph.add_edge("analysis", "impact")
    graph.add_edge("impact", "risk")

    # COMMON FLOW
    graph.add_edge("risk", "communication")
    graph.add_edge("communication", "compliance")

    graph.add_node("rag", rag_node)   # ✅ ADD

    graph.add_edge("research", "rag")          # NEW
    graph.add_edge("rag", "intelligence")      # NEW

    return graph.compile()


# -----------------------------
# ▶️ RUNNER
# -----------------------------
def run_orchestrator(query: str):

    app = build_graph()

    initial_state: AgentState = {
        "query": query,
        "research_data": [],
        "risk_data": {},
        "intelligence": {},
        "analysis": {},
        "impact": {},
        "route": "",
        "final_response": {},
        "compliance_status": "",
        "violations": []
    }

    result = app.invoke(initial_state)

    return result