import requests
import os

NEWS_KEY = os.getenv("NEWS_API_KEY")
GNEWS_KEY = os.getenv("GNEWS_API_KEY")
ALPHA_KEY = os.getenv("ALPHA_VANTAGE_KEY")


# -----------------------------
# HELPER: Deduplicate
# -----------------------------
def deduplicate_articles(articles):
    seen = set()
    unique = []

    for a in articles:
        title = a["title"]

        if title and title not in seen:
            seen.add(title)
            unique.append(a)

    return unique


# -----------------------------
# NEWSAPI FETCH
# -----------------------------
def fetch_newsapi():

    articles = []

    # 🇮🇳 INDIA NEWS
    india = requests.get(
        "https://newsapi.org/v2/top-headlines",
        params={
            "category": "business",
            "country": "in",
            "language": "en",
            "pageSize": 5,
            "apiKey": NEWS_KEY
        }
    ).json()

    for a in india.get("articles", []):
        articles.append({
            "title": a["title"],
            "content": a.get("description"),
            "source": "NewsAPI",
            "region": "India"
        })

    # 🌍 GLOBAL NEWS
    global_news = requests.get(
        "https://newsapi.org/v2/everything",
        params={
            "q": "stock market OR economy OR inflation OR fed",
            "language": "en",
            "pageSize": 5,
            "apiKey": NEWS_KEY
        }
    ).json()

    for a in global_news.get("articles", []):
        articles.append({
            "title": a["title"],
            "content": a.get("description"),
            "source": "NewsAPI",
            "region": "Global"
        })

    return articles


# -----------------------------
# GNEWS FETCH
# -----------------------------
def fetch_gnews():

    articles = []

    # 🇮🇳 INDIA
    india = requests.get(
        "https://gnews.io/api/v4/top-headlines",
        params={
            "category": "business",
            "lang": "en",
            "country": "in",
            "max": 5,
            "apikey": GNEWS_KEY
        }
    ).json()

    for a in india.get("articles", []):
        articles.append({
            "title": a["title"],
            "content": a.get("description"),
            "source": "GNews",
            "region": "India"
        })

    # 🌍 GLOBAL
    global_news = requests.get(
        "https://gnews.io/api/v4/search",
        params={
            "q": "stock market OR economy OR inflation OR fed",
            "lang": "en",
            "max": 5,
            "apikey": GNEWS_KEY
        }
    ).json()

    for a in global_news.get("articles", []):
        articles.append({
            "title": a["title"],
            "content": a.get("description"),
            "source": "GNews",
            "region": "Global"
        })

    return articles


# -----------------------------
# ALPHA VANTAGE NEWS
# -----------------------------
def fetch_alpha_news():

    articles = []

    response = requests.get(
        "https://www.alphavantage.co/query",
        params={
            "function": "NEWS_SENTIMENT",
            "apikey": ALPHA_KEY
        }
    ).json()

    for item in response.get("feed", [])[:5]:
        articles.append({
            "title": item["title"],
            "content": item.get("summary"),
            "source": "AlphaVantage",
            "region": "Global"
        })

    return articles


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def fetch_news():

    articles = []

    try:
        articles += fetch_newsapi()
    except Exception as e:
        print("NewsAPI Error:", e)

    try:
        articles += fetch_gnews()
    except Exception as e:
        print("GNews Error:", e)

    try:
        articles += fetch_alpha_news()
    except Exception as e:
        print("AlphaVantage Error:", e)

    # Deduplicate
    articles = deduplicate_articles(articles)

    return articles
