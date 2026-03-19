from langgraph.graph import StateGraph
from typing import TypedDict
from agents.research_agent import run_research_agent
from agents.risk_agent import run_risk_agent
from agents.communication_agent import generate_response
from agents.compliance_agent import run_compliance_agent


# -----------------------------
# STATE DEFINITION
# -----------------------------
class AgentState(TypedDict):
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

    query = state["query"].lower()

    # Portfolio-related keywords
    portfolio_keywords = [
        "my portfolio",
        "portfolio",
        "holdings",
        "allocation",
        "my investments"
    ]

    # If query is portfolio-focused → route differently
    if any(k in query for k in portfolio_keywords):
        return "portfolio_flow"

    # Default → market flow
    return "market_flow"

# -----------------------------
# NODES
# -----------------------------
def router_node(state: AgentState):

    decision = route_query(state)

    print(f"Routing decision: {decision}")

    return {
        **state,
        "route": decision
    }

def research_node(state: AgentState):

    print("Running Research Agent...")

    query = state["query"]

    result = run_research_agent()

    return {
        **state,
        "research_data": result
    }

def risk_node(state: AgentState):

    print("Running Risk Agent...")

    # later we will pass portfolio_id dynamically
    result = run_risk_agent()

    return {
        **state,
        "risk_data": result
    }

def communication_node(state: AgentState):

    print("Running Communication Agent...")

    response = generate_response(state)

    return {
        **state,
        "final_response": response
    }

def compliance_node(state: AgentState):

    result = run_compliance_agent(state)

    return result


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
            "portfolio_flow": "risk"   # later we add portfolio agent here
        }
    )

    # Market flow
    graph.add_edge("research", "risk")
    graph.add_edge("risk", "communication") 
    graph.add_edge("communication", "compliance")

    return graph.compile()

# -----------------------------
# RUNNER
# -----------------------------
def run_orchestrator(query: str):

    app = build_graph()

    result = app.invoke({
        "query": query
    })

    return result