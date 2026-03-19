import re

# -----------------------------
# SECTOR KEYWORDS
# -----------------------------
SECTOR_KEYWORDS = {
    "Banking": ["bank", "rbi", "loan", "interest rate", "nbfc"],
    "Technology": ["tech", "ai", "software", "chip", "semiconductor"],
    "Energy": ["oil", "crude", "gas", "energy", "opec"],
    "Healthcare": ["pharma", "hospital", "drug", "biotech"],
    "FMCG": ["consumer", "retail", "fmcg"],
    "Auto": ["auto", "car", "ev", "vehicle"],
    "Infrastructure": ["infra", "construction", "real estate"]
}


# -----------------------------
# EVENT KEYWORDS
# -----------------------------
EVENT_KEYWORDS = {
    "Rate Hike": ["rate hike", "interest rate increase"],
    "Rate Cut": ["rate cut", "interest rate decrease"],
    "M&A": ["acquisition", "merger", "buyout"],
    "Earnings": ["earnings", "quarter results", "profit"],
    "Policy Change": ["policy", "regulation", "ban", "approval"],
    "Geopolitical": ["war", "conflict", "sanctions"]
}


# -----------------------------
# DETECT SECTOR
# -----------------------------
def detect_sector(text):

    text = text.lower()

    for sector, keywords in SECTOR_KEYWORDS.items():
        for kw in keywords:
            if re.search(rf"\b{kw}\b", text):
                return sector

    return "Other"


# -----------------------------
# DETECT EVENTS
# -----------------------------
def detect_events(text):

    text = text.lower()

    events_found = []

    for event, keywords in EVENT_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                events_found.append(event)

    return events_found
