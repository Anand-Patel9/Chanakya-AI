def normalize_action(action_hint, sentiment=None, risk=None):
    if action_hint:
        a = action_hint.lower()

        # ✅ STRICT BUY (only explicit)
        if "buy" in a:
            return "BUY"

        # ✅ STRICT SELL
        if "sell" in a or "short" in a:
            return "SELL"

        # ❌ DO NOT treat "invest" as BUY
        # (too vague → causes wrong signals)

    # 🔥 FALLBACK INTELLIGENCE (PRIMARY LOGIC)

    if sentiment == "Negative" and risk == "High":
        return "SELL"

    if sentiment == "Positive" and risk in ["Low", "Medium"]:
        return "BUY"

    return "HOLD"