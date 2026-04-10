from services.risk_service import (
    calculate_returns,
    calculate_var,
    calculate_volatility,
    calculate_sector_exposure,
    stress_test,
    calculate_risk_score
)

def run_risk_agent(portfolio_id=None):

    from db.supabase_client import fetch_portfolio_holdings
    # -----------------------------
    # FETCH PORTFOLIO DATA
    # -----------------------------
    holdings = []

    if portfolio_id:
        holdings = fetch_portfolio_holdings(portfolio_id)

    # Fallback dummy data (for testing)
    if not holdings:
        holdings = [
            {"symbol": "AAPL", "sector": "Technology", "current_value": 50000},
            {"symbol": "JPM", "sector": "Finance", "current_value": 30000},
            {"symbol": "XOM", "sector": "Energy", "current_value": 20000}
        ]

    # -----------------------------
    # GENERATE PRICE SERIES (TEMP)
    # -----------------------------
    prices = [100 + i * 0.5 for i in range(100)]  # placeholder

    returns = calculate_returns(prices)

    # -----------------------------
    # RISK CALCULATIONS
    # -----------------------------
    var = calculate_var(returns)
    volatility = calculate_volatility(returns)
    sector_exposure = calculate_sector_exposure(holdings)

    total_value = sum(h["current_value"] for h in holdings)

    stress = stress_test(total_value)

    risk_score = calculate_risk_score(volatility, var)

    # -----------------------------
    # FINAL OUTPUT
    # -----------------------------
    result = {
        "value_at_risk": round(var, 4),
        "volatility": round(volatility, 4),
        "risk_score": risk_score,
        "sector_exposure": sector_exposure,
        "stress_test": stress
    }

    return result