import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -----------------------------
# 🧠 SAFE TEXT
# -----------------------------
def safe_text(x):
    if x is None:
        return ""
    if not isinstance(x, str):
        return str(x)
    return x.strip()


# -----------------------------
# 🧠 BUILD CONTEXT
# -----------------------------
def build_context(intel):

    context_blocks = []

    for d in intel.get("drivers", []):
        context_blocks.append(f"Driver: {safe_text(d)}")

    for n in intel.get("negative", []):
        context_blocks.append(f"Negative: {safe_text(n)}")

    for p in intel.get("positive", []):
        context_blocks.append(f"Positive: {safe_text(p)}")

    rag_data = intel.get("rag", "")
    if rag_data:
        context_blocks.append(f"Document Insight: {safe_text(rag_data)[:500]}")

    return "\n".join(context_blocks)


# -----------------------------
# 🛡️ GROUNDING CHECK
# -----------------------------
def is_grounded(output_text, context):

    context_words = set(context.lower().split())
    output_words = set(output_text.lower().split())

    overlap = context_words.intersection(output_words)

    blocked_terms = ["iran", "nuclear", "world war", "collapse"]

    for term in blocked_terms:
        if term in output_text.lower() and term not in context.lower():
            return False

    return len(overlap) >= 3


# -----------------------------
# 🚀 MAIN FUNCTION
# -----------------------------
def generate_market_analysis(intel):

    context = build_context(intel)
    print("🧠 CONTEXT SENT TO LLM:\n", context)

    if not context:
        return {
            "type": "market_update",
            "what_is_happening": "No strong market signals detected.",
            "why_it_is_happening": "Insufficient dominant macro drivers.",
            "what_to_do": "Wait for clearer market direction."
        }

    # -----------------------------
    # 🔥 BLOOMBERG-LEVEL PROMPT
    # -----------------------------
    prompt = f"""
You are a senior macro strategist at a global asset management firm.

DATA (STRICTLY USE ONLY THIS):
{context}

ANALYSIS RULES:
- Identify EXACTLY 1–2 dominant drivers
- Convert drivers into cause → market impact
- Mention sectors/assets where relevant
- NO generic phrases like "mixed signals" or "uncertainty"
- NO repeating same words

OUTPUT (STRICT JSON):

{{
  "what_is_happening": "Clear market movement with asset-level impact",
  "why_it_is_happening": "Cause → effect chain (e.g., oil ↑ → inflation ↑ → equities ↓)",
  "what_to_do": "Precise action (sector allocation / risk positioning)"
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        raw = safe_text(response.choices[0].message.content)
        print("🧠 RAW LLM OUTPUT:", raw)

        # -----------------------------
        # 🔧 FIX MARKDOWN JSON
        # -----------------------------
        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        parsed = json.loads(raw)

        what = safe_text(parsed.get("what_is_happening"))
        why = safe_text(parsed.get("why_it_is_happening"))
        action = safe_text(parsed.get("what_to_do"))

        # -----------------------------
        # 🔥 POST-PROCESSING (CRITICAL)
        # -----------------------------
        if "due to" in why.lower():
            why = why.replace("due to", "").strip()

        if len(why.split()) < 6:
            why = f"{why} impacting market conditions and investor sentiment"

        # 🔥 Improve action quality
        if "caution" in action.lower():
            action = "Reduce exposure to volatile sectors and increase allocation to defensive assets"

        combined = what + why + action

        # -----------------------------
        # 🛡️ GROUNDING CHECK
        # -----------------------------
        if not is_grounded(combined, context):
            print("⚠️ Weak grounding detected")

            macro = intel.get("macro", [])

            return {
                "type": "market_update",
                "what_is_happening": "Markets are reacting to key macro drivers.",
                "why_it_is_happening": f"Driven by {', '.join(macro)}.",
                "what_to_do": "Stay cautious and align portfolio with macro trends."
            }

        # -----------------------------
        # ✅ FINAL OUTPUT
        # -----------------------------
        return {
            "type": "market_update",
            "what_is_happening": what,
            "why_it_is_happening": why,
            "what_to_do": action
        }

    except Exception as e:
        print("❌ LLM ERROR:", e)

        return {
            "type": "market_update",
            "what_is_happening": "Markets are under pressure.",
            "why_it_is_happening": "Driven by key macroeconomic developments.",
            "what_to_do": "Maintain diversification and monitor risk exposure."
        }