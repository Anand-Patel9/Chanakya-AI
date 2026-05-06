import os
import json
import re
from groq import Groq


def clean_json(text):
    text = re.sub(r"```json|```", "", text).strip()
    text = re.sub(r"//.*", "", text)
    return text


def generate_insight(news_item):
    try:
        # ✅ CREATE CLIENT HERE (SAFE)
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        prompt = f"""
        Convert into STRICT JSON:

        Title: {news_item.get("title")}
        Description: {news_item.get("description")}

        Output ONLY JSON with:
        title, summary, sentiment, region, affected_sectors, risk_level, confidence_score, action_hint
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        raw = response.choices[0].message.content
        print("🔍 RAW:", raw)

        cleaned = clean_json(raw)

        return json.loads(cleaned)

    except Exception as e:
        print("❌ LLM Error:", e)
        return None


def normalize_sectors(insight):
    sectors = insight.get("affected_sectors", [])

    fixed = []
    for s in sectors:
        if "," in s:
            fixed.extend([x.strip() for x in s.split(",")])
        else:
            fixed.append(s.strip())

    insight["affected_sectors"] = fixed
    return insight