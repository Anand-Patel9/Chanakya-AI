import requests
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

print("NEWS API KEY:", NEWS_API_KEY)

def fetch_newsapi():
    try:
        url = f"https://newsapi.org/v2/everything?q=stock OR market OR finance OR economy&language=en&pageSize=20&apiKey={NEWS_API_KEY}"
        res = requests.get(url)
        data = res.json()

        articles = data.get("articles", [])
        print(f"🟢 NewsAPI fetched: {len(articles)}")

        return articles
    except Exception as e:
        print("❌ NewsAPI Error:", e)
        return []


def fetch_gnews():
    try:
        url = f"https://gnews.io/api/v4/search?q=stock market OR economy OR finance&lang=en&max=20&apikey={GNEWS_API_KEY}"
        res = requests.get(url)
        data = res.json()

        articles = data.get("articles", [])
        print(f"🟢 GNews fetched: {len(articles)}")

        return articles
    except Exception as e:
        print("❌ GNews Error:", e)
        return []


def fetch_finnhub():
    try:
        url = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API_KEY}"
        res = requests.get(url)
        data = res.json()

        print(f"🟢 Finnhub fetched: {len(data)}")

        return data
    except Exception as e:
        print("❌ Finnhub Error:", e)
        return []


def normalize_article(article):
    return {
        "title": article.get("title") or article.get("headline"),
        "description": article.get("description") or article.get("summary"),
    }


def get_all_news():
    all_news = []

    newsapi = fetch_newsapi()
    gnews = fetch_gnews()
    finnhub = fetch_finnhub()

    all_news.extend(newsapi)
    all_news.extend(gnews)
    all_news.extend(finnhub)

    # normalize
    cleaned = [normalize_article(a) for a in all_news if a]

    print(f"📰 TOTAL CLEANED NEWS: {len(cleaned)}")

    return cleaned