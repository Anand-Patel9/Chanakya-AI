from services.risk_service import (
    calculate_returns,
    calculate_var,
    calculate_volatility,
    calculate_sector_exposure,
    stress_test,
    calculate_risk_score
)

# 🔥 INTELLIGENCE IMPORTS
from services.risk_intelligence import aggregate_market_risk
from services.portfolio_risk_mapper import map_portfolio_risk
from services.concentration_risk import calculate_concentration_risk
from services.correlation_risk import calculate_correlation_risk
from services.event_risk import extract_event_risk

# 🔥 DECISION LAYER
from services.decision_engine import generate_portfolio_decisions
from services.rebalancer import suggest_rebalancing


def run_risk_agent(portfolio_id=None):

    from db.supabase_client import fetch_portfolio_holdings

    # -----------------------------
    # FETCH PORTFOLIO DATA
    # -----------------------------
    holdings = []

    if portfolio_id:
        holdings = fetch_portfolio_holdings(portfolio_id)

    # fallback (for testing)
    if not holdings:
        holdings = [
            {"symbol": "AAPL", "sector": "Technology", "current_value": 50000},
            {"symbol": "JPM", "sector": "Banking & Financial Services", "current_value": 30000},
            {"symbol": "XOM", "sector": "Energy", "current_value": 20000}
        ]

    # -----------------------------
    # PRICE SIMULATION (TEMP)
    # -----------------------------
    prices = [100 + i * 0.5 for i in range(100)]
    returns = calculate_returns(prices)

    # -----------------------------
    # CORE RISK METRICS
    # -----------------------------
    var = calculate_var(returns)
    volatility = calculate_volatility(returns)
    sector_exposure = calculate_sector_exposure(holdings)

    total_value = sum(h["current_value"] for h in holdings)

    stress = stress_test(total_value)

    risk_score = calculate_risk_score(volatility, var)

    # -----------------------------
    # MARKET INTELLIGENCE
    # -----------------------------
    market_risk = aggregate_market_risk()
    portfolio_risk_map = map_portfolio_risk(sector_exposure, market_risk)

    # -----------------------------
    # ADVANCED RISK LAYERS
    # -----------------------------
    concentration_risk = calculate_concentration_risk(sector_exposure)
    correlation_risk = calculate_correlation_risk(sector_exposure)
    event_risk = extract_event_risk()

    # -----------------------------
    # BASE RESULT
    # -----------------------------
    result = {
        "portfolio_value": total_value,

        # CORE METRICS
        "value_at_risk": round(var, 4),
        "volatility": round(volatility, 4),
        "risk_score": risk_score,

        # EXPOSURE
        "sector_exposure": sector_exposure,

        # MARKET INTELLIGENCE
        "market_risk": market_risk,
        "portfolio_risk_breakdown": portfolio_risk_map,

        # ADVANCED LAYERS
        "concentration_risk": concentration_risk,
        "correlation_risk": correlation_risk,
        "event_risk": event_risk,

        # STRESS
        "stress_test": stress
    }

    # -----------------------------
    # 🔥 DECISION LAYER (NEW)
    # -----------------------------
    decisions = generate_portfolio_decisions(result)

    rebalancing = suggest_rebalancing(sector_exposure)

    result.update({
        "decisions": decisions,
        "rebalancing_suggestions": rebalancing
    })

    return result