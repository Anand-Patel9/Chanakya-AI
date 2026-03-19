from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def store_news(article):

    supabase.table("market_news").insert({
        "title": article["title"],
        "content": article["content"],
        "source": article["source"],
        "sector": article.get("sector"),
        "sentiment": article.get("sentiment")
    }).execute()


def store_research_brief(data):

    supabase.table("research_insights").insert({
        "summary": data["summary"],
        "trend": data["trend"],
        "confidence_score": data["confidence"]
    }).execute()