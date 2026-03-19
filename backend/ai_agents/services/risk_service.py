import numpy as np


# -----------------------------
# CALCULATE RETURNS
# -----------------------------
def calculate_returns(prices):
    returns = np.diff(prices) / prices[:-1]
    return returns


# -----------------------------
# VALUE AT RISK (VaR)
# -----------------------------
def calculate_var(returns, confidence_level=0.95):
    return np.percentile(returns, (1 - confidence_level) * 100)


# -----------------------------
# VOLATILITY
# -----------------------------
def calculate_volatility(returns):
    return np.std(returns)


# -----------------------------
# SECTOR EXPOSURE
# -----------------------------
def calculate_sector_exposure(holdings):

    sector_totals = {}
    total_value = 0

    for h in holdings:
        sector = h.get("sector", "Other")
        value = h.get("current_value", 0)

        total_value += value

        if sector not in sector_totals:
            sector_totals[sector] = 0

        sector_totals[sector] += value

    # Convert to %
    for sector in sector_totals:
        sector_totals[sector] = round((sector_totals[sector] / total_value) * 100, 2)

    return sector_totals


# -----------------------------
# STRESS TEST
# -----------------------------
def stress_test(portfolio_value):

    return {
        "Market Crash (-20%)": round(portfolio_value * -0.2, 2),
        "Interest Rate Shock": round(portfolio_value * -0.07, 2),
        "Oil Price Spike": round(portfolio_value * -0.05, 2)
    }


# -----------------------------
# RISK SCORE
# -----------------------------
def calculate_risk_score(volatility, var):

    score = (abs(var) * 100) + (volatility * 100)

    return min(round(score, 2), 100)