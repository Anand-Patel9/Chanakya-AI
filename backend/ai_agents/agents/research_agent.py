import asyncio
from services.research_pipeline import run_research_pipeline


def run_research_agent():
    try:
        loop = asyncio.get_event_loop()

        if loop.is_running():
            # If already inside event loop (FastAPI case)
            result = asyncio.ensure_future(run_research_pipeline())
        else:
            result = loop.run_until_complete(run_research_pipeline())

        return result

    except Exception as e:
        raise Exception(f"Research Agent Error: {str(e)}")