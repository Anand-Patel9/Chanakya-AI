from collections import Counter


# -----------------------------
# 🧠 SAFE TEXT
# -----------------------------
def safe_text(x):
    if x is None:
        return ""
    if not isinstance(x, str):
        return str(x)
    return x.lower().strip()


# -----------------------------
# 🧠 KEYWORD → MACRO THEMES
# -----------------------------
KEYWORD_MAP = {
    # Energy
    "oil": "energy price volatility",
    "crude": "energy price volatility",
    "gas": "energy price volatility",

    # Geo
    "war": "geopolitical tensions",
    "conflict": "geopolitical tensions",
    "sanctions": "geopolitical tensions",
    "military": "geopolitical tensions",

    # Inflation
    "inflation": "inflation pressure",
    "cpi": "inflation pressure",

    # Rates
    "interest": "interest rate uncertainty",
    "rate": "interest rate uncertainty",
    "fed": "interest rate uncertainty",
    "central bank": "interest rate uncertainty",

    # Economy
    "recession": "economic slowdown",
    "slowdown": "economic slowdown",
    "growth": "economic slowdown",

    # Labor
    "jobs": "labor market weakness",
    "unemployment": "labor market weakness",

    # Tech
    "ai": "technology disruption",
    "chip": "technology disruption",
    "semiconductor": "technology disruption",

    # Finance
    "bank": "financial sector stress",
    "credit": "financial sector stress",

    # Market movement
    "selloff": "market correction",
    "fall": "market correction",
    "drop": "market correction",
    "rally": "market momentum"
}


# -----------------------------
# 🧠 EXTRACT MACRO THEMES
# -----------------------------
def extract_themes(text):
    themes = []

    for keyword, theme in KEYWORD_MAP.items():
        if keyword in text:
            themes.append(theme)

    return themes


# -----------------------------
# 🔥 DRIVER EXTRACTION (REAL INTEL)
# -----------------------------
def extract_drivers(text):

    drivers = []

    if "oil" in text or "crude" in text or "gas" in text:
        drivers.append("Rising oil prices impacting inflation and markets")

    if "war" in text or "conflict" in text or "iran" in text:
        drivers.append("Geopolitical conflict disrupting global stability")

    if "inflation" in text or "cpi" in text:
        drivers.append("Inflation pressures affecting interest rate expectations")

    if "interest" in text or "rate" in text or "fed" in text:
        drivers.append("Interest rate uncertainty impacting liquidity")

    if "ai" in text or "chip" in text or "semiconductor" in text:
        drivers.append("AI-driven volatility in technology stocks")

    if "recession" in text or "slowdown" in text:
        drivers.append("Economic slowdown concerns")

    if "bank" in text or "credit" in text:
        drivers.append("Financial sector stress and credit risks")

    return drivers


# -----------------------------
# 🚀 MAIN INTELLIGENCE BUILDER
# -----------------------------
def build_intelligence(research, web):

    negative = []
    positive = []

    macro_signals = []
    driver_signals = []

    # -----------------------------
    # 🔥 RESEARCH (HIGH WEIGHT)
    # -----------------------------
    for r in research[:20]:

        title = safe_text(r.get("title"))
        sentiment = safe_text(r.get("sentiment"))

        themes = extract_themes(title)
        drivers = extract_drivers(title)

        # 🔥 Weight research signals higher
        macro_signals.extend(themes * 2)
        driver_signals.extend(drivers * 2)

        if sentiment == "negative":
            negative.append(title)
        elif sentiment == "positive":
            positive.append(title)

    # -----------------------------
    # 🌐 WEB (LOW WEIGHT)
    # -----------------------------
    for w in web[:20]:

        title = safe_text(w.get("title"))

        themes = extract_themes(title)
        drivers = extract_drivers(title)

        macro_signals.extend(themes)
        driver_signals.extend(drivers)

    # -----------------------------
    # 🧠 MACRO SCORING
    # -----------------------------
    macro_counts = Counter(macro_signals)

    print("🧠 RAW MACRO COUNTS:", macro_counts)

    WEIGHTS = {
        "geopolitical tensions": 5,
        "energy price volatility": 5,
        "interest rate uncertainty": 4,
        "inflation pressure": 4,
        "financial sector stress": 4,
        "economic slowdown": 3,
        "market correction": 2,
        "technology disruption": 2,
        "market momentum": 1
    }

    scored_macro = []

    for theme, count in macro_counts.items():
        score = count * WEIGHTS.get(theme, 1)
        scored_macro.append((theme, score))

    scored_macro.sort(key=lambda x: x[1], reverse=True)

    top_macro = [theme for theme, _ in scored_macro[:3]]

    # -----------------------------
    # 🧠 DRIVER SCORING (CRITICAL)
    # -----------------------------
    driver_counts = Counter(driver_signals)

    print("🧠 RAW DRIVER COUNTS:", driver_counts)

    top_drivers = [d for d, c in driver_counts.items() if c >= 2]

    # fallback if weak signals
    if not top_drivers:
        top_drivers = list(driver_counts.keys())[:3]

    # -----------------------------
    # 🧠 FINAL INTELLIGENCE OUTPUT
    # -----------------------------
    intel = {
        "negative": negative[:5],
        "positive": positive[:5],
        "macro": top_macro[:3],
        "drivers": top_drivers[:3]
    }

    print("🔥 FINAL INTEL:", intel)

    return intel