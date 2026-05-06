from services.research_service import get_insights
from services.sector_mapper import map_sectors


def extract_event_risk():
    insights = get_insights().data or []

    events = []

    for ins in insights:
        if ins.get("risk_level") == "High":
            events.append({
                "title": ins.get("title"),
                "sector": map_sectors(ins.get("affected_sectors", [])),  # ✅ FIX
                "impact": "High"
            })

    # ✅ DEDUPLICATION
    seen = set()
    unique_events = []

    for e in events:
        key = e["title"]

        if key not in seen:
            seen.add(key)
            unique_events.append(e)

    return unique_events[:5]