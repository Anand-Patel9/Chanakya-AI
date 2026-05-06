def basic_score(i):
    return (
        (3 if i.get("risk_level") == "high" else 2 if i.get("risk_level") == "medium" else 1)
        + (2 if i.get("sentiment") == "negative" else 1)
        + i.get("confidence_score", 0)
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

    # Confidence
    score += i.get("confidence_score", 0)

    # Sector boost
    sectors = i.get("affected_sectors", [])

    if "Banking & Financial Services" in sectors:
        score += 3
    if "Energy" in sectors:
        score += 2

    return score


# ✅ THIS FUNCTION WAS MISSING (CRITICAL)
def rank_insights(insights):
    return sorted(insights, key=advanced_score, reverse=True)