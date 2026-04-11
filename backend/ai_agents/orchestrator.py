from langgraph.graph import StateGraph
from typing import TypedDict
from agents.research_agent import run_research_agent
from agents.risk_agent import run_risk_agent
from agents.communication_agent import run_communication_agent


# -----------------------------
# STATE DEFINITION
# -----------------------------
class AgentState(TypedDict, total=False):
    query: str
    research_data: dict
    risk_data: dict
    route: str
    final_response: str
    compliance_status: str
    violations: list


# -----------------------------
# ROUTER FUNCTION
# -----------------------------
def route_query(state: AgentState):

    query = state.get("query", "").lower()

    portfolio_keywords = [
        "portfolio", "holdings", "allocation", "investments"
    ]

    if any(k in query for k in portfolio_keywords):
        return "portfolio_flow"

    return "market_flow"


# -----------------------------
# NODES
# -----------------------------
def router_node(state: AgentState):

    decision = route_query(state)

    print(f"Routing decision: {decision}")

    return {**state, "route": decision}


def research_node(state: AgentState):

    print("Running Research Agent...")

    try:
        result = run_research_agent(state["query"])
    except Exception as e:
        result = {"error": str(e)}

    return {**state, "research_data": result}


def risk_node(state: AgentState):

    print("Running Risk Agent...")

    try:
        result = run_risk_agent()
    except Exception as e:
        result = {"error": str(e)}

    return {**state, "risk_data": result}


def communication_node(state: AgentState):

    print("Running Communication Agent...")

    try:
        response = run_communication_agent(
            state["query"],
            state.get("research_data"),
            state.get("risk_data")
        )
    except Exception as e:
        response = {"response": f"Error: {str(e)}"}

    return {**state, "final_response": response}


def compliance_node(state: AgentState):

    print("Running Compliance Agent...")

    try:
        # ✅ LAZY IMPORT (prevents startup crash)
        from agents.compliance_agent import run_compliance_agent

        return run_compliance_agent(state)

    except Exception as e:
        return {
            **state,
            "compliance_status": "error",
            "violations": [str(e)]
        }


# -----------------------------
# GRAPH SETUP
# -----------------------------
def build_graph():

    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("router", router_node)
    graph.add_node("research", research_node)
    graph.add_node("risk", risk_node)
    graph.add_node("communication", communication_node)
    graph.add_node("compliance", compliance_node)

    # Start
    graph.add_edge("__start__", "router")

    # Conditional routing
    graph.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {
            "market_flow": "research",
            "portfolio_flow": "risk"
        }
    )

    # Flow
    graph.add_edge("research", "risk")
    graph.add_edge("risk", "communication")
    graph.add_edge("communication", "compliance")

    return graph.compile()


# -----------------------------
# RUNNER
# -----------------------------
def run_orchestrator(query: str):

    app = build_graph()

    initial_state = {
        "query": query,
        "research_data": {},
        "risk_data": {},
        "route": "",
        "final_response": "",
        "compliance_status": "",
        "violations": []
    }

    result = app.invoke(initial_state)

    return result