import asyncio
from services.news_service import fetch_news
from services.market_service import fetch_market_data
from services.sentiment_service import analyze_sentiment
from services.event_detector import detect_sector, detect_events
from services.summarizer import summarize
from db.supabase_client import store_news, store_research_brief


# -----------------------------
# DEDUPLICATION
# -----------------------------
def deduplicate_articles(articles):
    seen = set()
    unique = []

    for a in articles:
        title = a["title"]

        if title not in seen:
            seen.add(title)
            unique.append(a)

    return unique


# -----------------------------
# PROCESS SINGLE ARTICLE
# -----------------------------
def process_article(article):
    title = article["title"]

    sentiment, score = analyze_sentiment(title)
    sector = detect_sector(title)
    events = detect_events(title)

    summary = summarize(article["content"] or title)

    relevance_score = min(score + 0.3, 1.0)

    processed = {
        "title": title,
        "content": summary,
        "source": article["source"],
        "sector": sector,
        "sentiment": sentiment,
        "relevance_score": relevance_score
    }

    store_news(processed)

    return processed

# -----------------------------
# SECTOR TREND ENGINE
# -----------------------------
def calculate_sector_trends(processed_articles):

    sector_scores = {}

    for article in processed_articles:

        sector = article["sector"]
        sentiment = article["sentiment"]

        score = 1 if sentiment == "Bullish" else -1 if sentiment == "Bearish" else 0

        if sector not in sector_scores:
            sector_scores[sector] = 0

        sector_scores[sector] += score

    sector_trends = {}

    for sector, value in sector_scores.items():

        if value > 0:
            sector_trends[sector] = "Bullish"
        elif value < 0:
            sector_trends[sector] = "Bearish"
        else:
            sector_trends[sector] = "Neutral"

    return sector_trends

# -----------------------------
# MAIN PIPELINE
# -----------------------------
async def run_research_pipeline():

    # Async execution
    news_task = asyncio.to_thread(fetch_news)
    market_task = asyncio.to_thread(fetch_market_data)

    news, market = await asyncio.gather(news_task, market_task)

    # Deduplicate
    news = deduplicate_articles(news)

    processed_articles = []

    combined_titles = ""

    for article in news:
        processed = process_article(article)
        processed_articles.append(processed)
        combined_titles += article["title"] + " "
        sector_trends = calculate_sector_trends(processed_articles)

    # Overall sentiment
    overall_trend, confidence = analyze_sentiment(combined_titles)

    # Generate research brief
    research_brief = f"""
Market Intelligence Brief

Overall Market Trend: {overall_trend}
Confidence Score: {confidence}

Sector Trends:
{chr(10).join([f"{k}: {v}" for k, v in sector_trends.items()])}

Top Headlines:
{chr(10).join([a["title"] for a in processed_articles[:5]])}
"""

    store_research_brief({
        "summary": research_brief,
        "trend": overall_trend,
        "confidence": confidence
    })

    return {
        "trend": overall_trend,
        "confidence": confidence,
        "market_data": market,
        "sector_trends": sector_trends,
        "articles_processed": len(processed_articles),
        "top_articles": processed_articles[:5],
        "brief": research_brief
    }