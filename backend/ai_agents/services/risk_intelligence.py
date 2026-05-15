from ai_agents.services.research_service import get_insights
from ai_agents.services.sector_mapper import map_sectors


def aggregate_market_risk(insights=None):

    # ✅ USE PASSED DATA (OPTIMIZED FLOW)
    if not insights:
        insights = get_insights().data or []

    sector_risk = {}
    risk_weights = {"Low": 1, "Medium": 2, "High": 3}

    for ins in insights:
        sectors = ins.get("affected_sectors", [])
        sectors = map_sectors(sectors)

        if not isinstance(sectors, list):
            continue

        # ✅ FIX: define risk
        risk = ins.get("risk_level", "Low")

        for s in sectors:
            if s not in sector_risk:
                sector_risk[s] = 0

            sector_risk[s] += risk_weights.get(risk, 1)

    # -----------------------------
    # NORMALIZE
    # -----------------------------
    final = {}

    for sector, score in sector_risk.items():
        if score >= 6:
            final[sector] = "High"
        elif score >= 3:
            final[sector] = "Medium"
        else:
            final[sector] = "Low"

    return final