def map_portfolio_risk(sector_exposure, market_risk):

    mapped = []

    for sector, exposure in sector_exposure.items():

        risk = market_risk.get(sector, "Low")

        mapped.append({
            "sector": sector,
            "exposure_percent": exposure,
            "market_risk": risk
        })

    return mapped