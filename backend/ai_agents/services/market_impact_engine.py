def build_market_impact(intel):

    impact = {
        "equities": None,
        "bonds": None,
        "commodities": None,
        "sectors": []
    }

    drivers = intel.get("drivers", [])

    for d in drivers:

        d = d.lower()

        if "geopolitical" in d:
            impact["equities"] = "down"
            impact["bonds"] = "up"
            impact["commodities"] = "up"
            impact["sectors"].append("defense")

        if "ai" in d or "technology" in d:
            impact["sectors"].append("technology volatility")

        if "oil" in d:
            impact["commodities"] = "up"

    return impact