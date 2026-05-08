def safe_text(x):
    if not x:
        return ""
    return str(x).lower()


# -----------------------------
# 🎯 FILTER RELEVANT SIGNALS
# -----------------------------
def is_market_relevant(title):

    keywords = [
        "market", "stock", "inflation", "interest", "rate",
        "oil", "economy", "fed", "war", "growth", "recession"
    ]

    t = safe_text(title)

    return any(k in t for k in keywords)


# -----------------------------
# 🧠 CLASSIFY SIGNAL
# -----------------------------
def classify_signal(title):

    t = safe_text(title)

    if any(k in t for k in ["war", "oil", "inflation", "rate", "crisis"]):
        return "negative"

    if any(k in t for k in ["rally", "growth", "record", "gain"]):
        return "positive"

    return "neutral"


# -----------------------------
# 🧠 BUILD INTELLIGENCE
# -----------------------------
def build_intelligence(research, web):

    negative = []
    positive = []
    macro = []

    keywords_map = {
        "oil": "energy price volatility",
        "war": "geopolitical tensions",
        "inflation": "inflation pressure",
        "rate": "interest rate uncertainty",
        "recession": "economic slowdown",
        "ai": "technology disruption"
    }

    # -----------------------------
    # 🔍 ANALYZE RESEARCH (STRONG SIGNAL)
    # -----------------------------
    for r in research[:10]:

        title = (r.get("title") or "").lower()
        sentiment = (r.get("sentiment") or "").lower()

        for key, theme in keywords_map.items():
            if key in title:
                macro.append(theme)

        if sentiment == "negative":
            negative.append(title)

        elif sentiment == "positive":
            positive.append(title)

    # -----------------------------
    # 🔍 ANALYZE WEB (SUPPORTING SIGNAL)
    # -----------------------------
    for w in web[:10]:

        title = (w.get("title") or "").lower()

        for key, theme in keywords_map.items():
            if key in title:
                macro.append(theme)

    # -----------------------------
    # 🧠 CLUSTER (IMPORTANT)
    # -----------------------------
    from collections import Counter

    macro_counts = Counter(macro)

    # 🔥 pick top themes only
    top_macro = [m for m, count in macro_counts.items() if count >= 2]

    return {
        "negative": negative[:5],
        "positive": positive[:5],
        "macro": top_macro[:3]   # 🔥 ONLY STRONG THEMES
    }