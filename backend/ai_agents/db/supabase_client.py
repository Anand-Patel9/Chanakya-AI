from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# -----------------------------
# STORE NEWS
# -----------------------------
def store_news(article):
    try:
        supabase.table("market_news").insert({
            "title": article["title"],
            "content": article["content"],
            "source": article["source"],
            "sentiment_score": article.get("relevance_score", 0),
            "publish_date": None
        }).execute()
    except Exception as e:
        print("Error storing news:", e)


# -----------------------------
# STORE RESEARCH BRIEF
# -----------------------------
def store_research_brief(data):
    try:
        supabase.table("research_insights").insert({
            "summary": data["summary"],
            "relevance_score": data.get("confidence", 0),
            "portfolio_id": None,
            "news_id": None
        }).execute()
    except Exception as e:
        print("Error storing research brief:", e)


# -----------------------------
# FETCH PORTFOLIO HOLDINGS
# -----------------------------
def fetch_portfolio_holdings(portfolio_id):
    try:
        # 🔥 Validate portfolio_id (UUID should be long string)
        if not portfolio_id or len(str(portfolio_id)) < 10:
            print("⚠️ Invalid portfolio_id, using fallback")
            return []

        response = supabase.table("portfolio_holdings") \
            .select("*") \
            .eq("portfolio_id", portfolio_id) \
            .execute()

        # 🔥 Handle empty response safely
        if not response.data:
            print("⚠️ No holdings found for portfolio_id:", portfolio_id)
            return []

        return response.data

    except Exception as e:
        print("❌ DB Error in fetch_portfolio_holdings:", e)
        return []
# -----------------------------
# STORE COMPLIANCE REPORT
# -----------------------------
def store_compliance_log(data):

    try:
        supabase.table("portfolio_compliance_checks").insert({
            "portfolio_id": data.get("portfolio_id"),
            "check_type": "Communication Review",
            "status": data["status"],
            "violation_details": ", ".join(data["violations"]),
            "approved_by": None
        }).execute()
    except Exception as e:
        print("Error storing portfolio_compliance_checks:", e)