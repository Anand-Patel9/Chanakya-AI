from fastapi import APIRouter
from ai_agents.agents.research_agent import run_research_agent
from ai_agents.services.research_service import get_insights

router = APIRouter(prefix="/research", tags=["Research"])

# ✅ EXISTING
@router.post("/generate")
def generate():
    return run_research_agent()


# ✅ ADD THIS NEW ENDPOINT
@router.get("/insights")
def fetch_insights():
    data = get_insights()

    # Supabase returns .data
    return data.data if hasattr(data, "data") else data