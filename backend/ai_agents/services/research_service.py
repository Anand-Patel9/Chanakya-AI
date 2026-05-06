from supabase import create_client
import os

def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # ✅ CORRECT KEY

    if not key:
        raise Exception("SUPABASE_SERVICE_ROLE_KEY is missing")

    return create_client(url, key)


def store_news(news_list):
    supabase = get_supabase()
    supabase.table("market_news").insert(news_list).execute()


def store_insights(insights):
    if not insights:
        return

    # 🚨 REMOVE invalid entries
    insights = [i for i in insights if isinstance(i, dict)]

    if not insights:
        print("⚠️ No valid insights to insert")
        return

    supabase = get_supabase()

    try:
        supabase.table("portfolio_research_insights").insert(insights).execute()
    except Exception as e:
        print("❌ INSERT ERROR:", e)


def get_insights():
    supabase = get_supabase()
    return supabase.table("portfolio_research_insights").select("*").execute()