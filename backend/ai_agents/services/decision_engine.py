def generate_portfolio_decisions(risk_data):

    decisions = []

    # -----------------------------
    # 1. MARKET RISK BASED ACTION
    # -----------------------------
    for item in risk_data.get("portfolio_risk_breakdown", []):
        risk = item.get("market_risk", "Low")
        exposure = item.get("exposure_percent", 0)
        sector = item.get("sector")

        if risk == "High" and exposure > 40:
            action = "REDUCE"
        elif risk == "High":
            action = "HEDGE"
        elif risk == "Medium":
            action = "MONITOR"
        else:
            action = "HOLD"

        decisions.append({
            "action": action,
            "sector": sector,
            "reason": f"{risk} market risk",
            "confidence": 0.8
        })

    # -----------------------------
    # 2. CONCENTRATION RISK
    # -----------------------------
    for c in risk_data.get("concentration_risk", []):
        if c.get("risk") == "High":
            decisions.append({
                "action": "REDUCE",
                "sector": c.get("sector"),
                "reason": "Overexposed sector",
                "confidence": 0.85
            })

    # -----------------------------
    # 3. EVENT RISK
    # -----------------------------
    for e in risk_data.get("event_risk", []):
        decisions.append({
            "action": "HEDGE",
            "sector": ", ".join(e.get("sector", [])),
            "reason": f"Event risk: {e.get('title')}",
            "confidence": 0.75
        })

    # ✅ REMOVE DUPLICATES (FIXED POSITION)
    seen = set()
    unique = []

    for d in decisions:
        key = (d["action"], d["sector"])

        if key not in seen:
            seen.add(key)
            unique.append(d)

    return unique