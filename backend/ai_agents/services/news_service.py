import requests
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")


def fetch_news():

    newsapi_url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={NEWS_API_KEY}"
    
    gnews_url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&token={GNEWS_API_KEY}"

    newsapi_articles = []
    gnews_articles = []

    # ---------------------------
    # NewsAPI
    # ---------------------------
    try:
        res1 = requests.get(newsapi_url)
        data1 = res1.json()

        for a in data1.get("articles", []):
            newsapi_articles.append({
                "title": a.get("title"),
                "content": a.get("description"),
                "source": "NewsAPI"
            })

    except Exception as e:
        print("NewsAPI Error:", e)

    # ---------------------------
    # GNews
    # ---------------------------
    try:
        res2 = requests.get(gnews_url)
        data2 = res2.json()

        for a in data2.get("articles", []):
            gnews_articles.append({
                "title": a.get("title"),
                "content": a.get("description"),
                "source": "GNews"
            })

    except Exception as e:
        print("GNews Error:", e)

    # ---------------------------
    # MERGE BOTH
    # ---------------------------
    all_news = newsapi_articles + gnews_articles

    return all_news