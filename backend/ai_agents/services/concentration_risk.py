def calculate_concentration_risk(sector_exposure):

    high_concentration = []

    for sector, percent in sector_exposure.items():
        if percent > 40:
            high_concentration.append({
                "sector": sector,
                "exposure": percent,
                "risk": "High"
            })
        elif percent > 25:
            high_concentration.append({
                "sector": sector,
                "exposure": percent,
                "risk": "Medium"
            })

    return high_concentration