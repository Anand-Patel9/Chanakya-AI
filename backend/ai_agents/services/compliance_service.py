def check_compliance(data):

    violations = []

    # -----------------------------
    # TEXT RULES (YOUR EXISTING)
    # -----------------------------
    text = str(data)
    text_lower = text.lower()

    if "guaranteed return" in text_lower:
        violations.append("Illegal guarantee of returns")

    if "risk-free" in text_lower:
        violations.append("Misleading risk-free claim")

    if "double your money" in text_lower:
        violations.append("Unrealistic promise")

    if "no risk" in text_lower:
        violations.append("Missing risk disclosure")

    # -----------------------------
    # PORTFOLIO RULES (NEW)
    # -----------------------------
    sector_exposure = data.get("sector_exposure", {})
    risk_score = data.get("risk_score", 0)

    # Rule 1: No sector > 40%
    for sector, value in sector_exposure.items():
        if value > 40:
            violations.append(f"{sector} exposure too high ({value}%)")

    # Rule 2: Risk score threshold
    if risk_score > 75:
        violations.append("Portfolio risk too high")

    # Rule 3: Over-concentration
    if len(sector_exposure) < 2:
        violations.append("Portfolio not diversified")

    # -----------------------------
    # RESULT
    # -----------------------------
    if violations:
        return {
            "status": "Failed",
            "violations": violations
        }

    return {
        "status": "Approved",
        "violations": []
    }