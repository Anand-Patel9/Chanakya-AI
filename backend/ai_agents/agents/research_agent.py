import asyncio
from services.research_pipeline import run_research_pipeline


def run_research_agent():
    """
    Entry point for Research Agent
    Called by API / Controller
    """

    result = asyncio.run(run_research_pipeline())

    return result