def basic_score(i):
    confidence = i.get("confidence_score") or 0

    return (
        (3 if i.get("risk_level") == "high" else 2 if i.get("risk_level") == "medium" else 1)
        + (2 if i.get("sentiment") == "negative" else 1)
        + confidence
    )


def advanced_score(i):
    score = 0

    # Risk weight
    if i.get("risk_level") == "high":
        score += 5
    elif i.get("risk_level") == "medium":
        score += 3
    else:
        score += 1

    # Sentiment weight
    if i.get("sentiment") == "negative":
        score += 4
    elif i.get("sentiment") == "positive":
        score += 2

    # ✅ SAFE CONFIDENCE (FIX)
    confidence = i.get("confidence_score") or 0
    score += confidence

    # Sector boost
    sectors = i.get("affected_sectors", []) or []

    if "Banking & Financial Services" in sectors:
        score += 3
    if "Energy" in sectors:
        score += 2

    return score


# ✅ THIS FUNCTION WAS MISSING (CRITICAL)
def rank_insights(insights):
    return sorted(insights, key=advanced_score, reverse=True)