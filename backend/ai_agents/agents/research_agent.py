import asyncio
from services.research_pipeline import run_research_pipeline


def run_research_agent(query):
    """
    Entry point for Research Agent
    """

    try:
        # ✅ Correct way (works inside FastAPI)
        result = asyncio.run(run_research_pipeline(query))
        return result

    except Exception as e:
        raise Exception(f"Research Agent Error: {str(e)}")