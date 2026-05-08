import requests
import os
from services.news_service import fetch_newsapi, fetch_gnews, fetch_finnhub


# -----------------------------
# 🧠 FINANCE FILTER
# -----------------------------
def is_finance_news(article):
    keywords = [
        "stock", "market", "economy", "inflation", "interest",
        "oil", "war", "fed", "rates", "gdp", "recession", "bond"
    ]

    text = ((article.get("title") or "") + (article.get("description") or "")).lower()

    return any(k in text for k in keywords)


# -----------------------------
# 🚀 MAIN SEARCH FUNCTION
# -----------------------------
def search_web(query):

    news = fetch_newsapi(query)      # must accept query
    gnews = fetch_gnews(query)       # must accept query
    finnhub = fetch_finnhub()        # no query needed

    combined = news + gnews + finnhub

    # ✅ FILTER FINANCE NEWS (YOU MISSED THIS EARLIER)
    filtered = [n for n in combined if is_finance_news(n)]

    # ✅ REMOVE DUPLICATES
    seen = set()
    clean = []

    for n in filtered:
        title = n.get("title")
        if title and title not in seen:
            seen.add(title)
            clean.append(n)

    print(f"📰 FINAL NEWS COUNT: {len(clean)}")

    return clean[:10]