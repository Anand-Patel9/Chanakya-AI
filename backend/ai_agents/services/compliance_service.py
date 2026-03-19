def check_compliance(text):

    violations = []

    text_lower = text.lower()

    # -----------------------------
    # RULES
    # -----------------------------
    if "guaranteed return" in text_lower:
        violations.append("Illegal guarantee of returns")

    if "risk-free" in text_lower:
        violations.append("Misleading risk-free claim")

    if "double your money" in text_lower:
        violations.append("Unrealistic promise")

    if "no risk" in text_lower:
        violations.append("Missing risk disclosure")

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