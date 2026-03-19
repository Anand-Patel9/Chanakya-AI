import numpy as np

def calculate_var(returns, confidence_level=0.95):
    return np.percentile(returns, (1 - confidence_level) * 100)

def run_risk_agent():

    # Example portfolio returns
    returns = np.random.normal(0.001, 0.02, 1000)

    var = calculate_var(returns)

    volatility = np.std(returns)

    sector_exposure = {
        "Technology": 35,
        "Finance": 20,
        "Healthcare": 15,
        "Energy": 10,
        "Consumer": 20
    }

    crash_test = {
        "Market Crash (-20%)": -18.5,
        "Interest Rate Shock": -6.2,
        "Oil Price Spike": -4.1
    }

    result = {
        "value_at_risk": round(var,4),
        "volatility": round(volatility,4),
        "sector_exposure": sector_exposure,
        "stress_test": crash_test
    }

    return result