import requests
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")


# -----------------------------
# 🔧 NORMALIZER (COMMON FORMAT)
# -----------------------------
def normalize_article(article):
    return {
        "title": article.get("title") or article.get("headline"),
        "description": article.get("description") or article.get("summary"),
        "source": article.get("source", {}).get("name") if isinstance(article.get("source"), dict) else article.get("source"),
        "url": article.get("url")
    }


# -----------------------------
# 📰 NEWSAPI
# -----------------------------
def fetch_newsapi(query):
    try:
        url = "https://newsapi.org/v2/everything"

        params = {
            "q": query or "stock market economy finance",
            "language": "en",
            "pageSize": 20,
            "apiKey": NEWS_API_KEY
        }

        res = requests.get(url, params=params).json()
        articles = res.get("articles", [])

        print(f"🟢 NewsAPI fetched: {len(articles)}")

        return [normalize_article(a) for a in articles]

    except Exception as e:
        print("❌ NewsAPI Error:", e)
        return []


# -----------------------------
# 🌍 GNEWS
# -----------------------------
def fetch_gnews(query):
    try:
        url = "https://gnews.io/api/v4/search"

        params = {
            "q": query or "stock market economy finance",
            "lang": "en",
            "max": 20,
            "token": GNEWS_API_KEY
        }

        res = requests.get(url, params=params).json()
        articles = res.get("articles", [])

        print(f"🟢 GNews fetched: {len(articles)}")

        return [normalize_article(a) for a in articles]

    except Exception as e:
        print("❌ GNews Error:", e)
        return []


# -----------------------------
# 📊 FINNHUB
# -----------------------------
def fetch_finnhub():
    try:
        url = "https://finnhub.io/api/v1/news"

        params = {
            "category": "general",
            "token": FINNHUB_API_KEY
        }

        res = requests.get(url, params=params).json()

        print(f"🟢 Finnhub fetched: {len(res)}")

        return [normalize_article(a) for a in res[:20]]

    except Exception as e:
        print("❌ Finnhub Error:", e)
        return []


# -----------------------------
# 🚀 AGGREGATOR (OPTIONAL USE)
# -----------------------------
def get_all_news(query="stock market"):
    newsapi = fetch_newsapi(query)
    gnews = fetch_gnews(query)
    finnhub = fetch_finnhub()

    combined = newsapi + gnews + finnhub

    print(f"📰 TOTAL NEWS: {len(combined)}")

    return combined