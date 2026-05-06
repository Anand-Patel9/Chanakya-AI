def suggest_rebalancing(sector_exposure):

    suggestions = []

    for sector, percent in sector_exposure.items():

        if percent > 40:
            suggestions.append({
                "sector": sector,
                "current": percent,
                "suggested": 25,
                "action": "Reduce allocation"
            })

        elif percent < 10:
            suggestions.append({
                "sector": sector,
                "current": percent,
                "suggested": 15,
                "action": "Increase allocation"
            })

    return suggestions