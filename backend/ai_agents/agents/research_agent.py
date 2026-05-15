from ai_agents.services.news_service import get_all_news
from ai_agents.services.llm_service import generate_insight, normalize_sectors
from ai_agents.services.research_service import store_insights
from ai_agents.services.ranking_service import rank_insights
from ai_agents.services.region_service import classify_region
from ai_agents.services.sector_mapper import map_sectors   # ✅ FIXED IMPORT
from ai_agents.services.action_mapper import normalize_action   # ✅ NEW IMPORT
from ai_agents.services.research_service import store_insights, get_insights  # ✅ NEW IMPORT


# -----------------------------
# CACHE CHECK
# -----------------------------



def run_research_agent():
    try:
        print("🚀 Running Research Agent...")

        cached = get_insights().data or []

        if cached and len(cached) > 0:
            print("⚡ Using cached insights")
            return cached[:5]   # limit like your normal output

        news = get_all_news()
        print(f"📰 Fetched {len(news)} news")

        insights = []
        seen = set()

        for item in news[:8]:
            try:
                title = item.get("title")

                # ✅ DUPLICATE FILTER
                if not title or title in seen:
                    continue

                seen.add(title)

                insight = generate_insight(item)

                # ✅ SAFETY CHECK
                if not isinstance(insight, dict):
                    continue

                # ✅ CLEAN SECTORS FROM LLM
                insight = normalize_sectors(insight)

                # ✅ Normalize risk levels (IMPORTANT)
                risk = insight.get("risk_level", "").lower()

                if "moderate" in risk:
                    insight["risk_level"] = "Medium"
                elif "high" in risk:
                    insight["risk_level"] = "High"
                elif "low" in risk:
                    insight["risk_level"] = "Low"

                # ✅ Action standardization
                insight["action"] = normalize_action(
                    insight.get("action_hint"),
                    insight.get("sentiment"),
                    insight.get("risk_level")
                )

                # ✅ Finance-only filter
                valid_sectors = [
                    "Banking & Financial Services",
                    "IT",
                    "Energy",
                    "Auto",
                    "Cryptocurrency"
                ]

                filtered_sectors = [
                    s for s in insight.get("affected_sectors", [])
                    if s in valid_sectors
                ]

                if not filtered_sectors:
                    continue

                insight["affected_sectors"] = filtered_sectors

                if not any(s in valid_sectors for s in insight.get("affected_sectors", [])):
                    continue

                # ✅ NEW FEATURE 1: REGION CLASSIFICATION
                insight["market_scope"] = classify_region(
                    insight.get("region")
                )

                # ✅ NEW FEATURE 2: SECTOR STANDARDIZATION
                insight["affected_sectors"] = map_sectors(
                    insight.get("affected_sectors", [])
                )

                # ✅ RELAXED FILTER (DON’T KILL DATA)
                if not insight.get("affected_sectors"):
                    continue

                if insight.get("confidence_score", 0) < 0.3:
                    continue

                insights.append(insight)
                print("✅ Accepted:", insight["title"])

            except Exception as e:
                print("❌ LLM Error:", e)

        print(f"📊 Generated {len(insights)} insights")

        # ✅ RANKING
        ranked = rank_insights(insights)

        # ✅ LIMIT TOP 5
        ranked = ranked[:5]

        # ✅ STORE IN DB
        if ranked:
            store_insights(ranked)
            print("✅ Stored in DB")

        return ranked

    except Exception as e:
        print("🔥 AGENT CRASH:", e)
        return {"error": str(e)}