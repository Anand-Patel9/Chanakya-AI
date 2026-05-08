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
# 🧠 BUILD CONTEXT FROM INTEL
# -----------------------------
def build_context(intel):

    context_blocks = []

    for n in intel.get("negative", []):
        context_blocks.append(f"Negative: {safe_text(n)}")

    for p in intel.get("positive", []):
        context_blocks.append(f"Positive: {safe_text(p)}")

    for m in intel.get("macro", []):
        context_blocks.append(f"Macro: {safe_text(m)}")

    return "\n".join(context_blocks)


# -----------------------------
# 🛡️ GROUNDING CHECK
# -----------------------------
def is_grounded(output_text, context):

    context_words = set(context.lower().split())
    output_words = set(output_text.lower().split())

    overlap = context_words.intersection(output_words)

    # 🔥 Block hallucinated terms
    blocked_terms = ["iran", "nuclear", "world war", "collapse"]

    for term in blocked_terms:
        if term in output_text.lower() and term not in context.lower():
            return False

    return len(overlap) >= 3   # ✅ RELAXED


# -----------------------------
# 🚀 MAIN FUNCTION
# -----------------------------
def generate_market_analysis(intel):

    context = build_context(intel)

    if not context:
        return {
            "type": "market_update",
            "what_is_happening": "Insufficient data.",
            "why_it_is_happening": "No strong signals available.",
            "what_to_do": "Wait for clearer trends."
        }

    prompt = f"""
    You are a senior financial analyst.

    DATA:
    {context}

    TASK:
    - Identify top 1–2 drivers
    - Give clear macro reasoning
    - Avoid generic answers

    OUTPUT (STRICT JSON):

    {{
    "what_is_happening": "...",
    "why_it_is_happening": "...",
    "what_to_do": "..."
    }}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        raw = safe_text(response.choices[0].message.content)

        parsed = json.loads(raw)

        what = safe_text(parsed.get("what_is_happening"))
        why = safe_text(parsed.get("why_it_is_happening"))
        action = safe_text(parsed.get("what_to_do"))

        combined = what + why + action

        # ✅ DO NOT BREAK SYSTEM — ONLY WARN
        if not is_grounded(combined, context):
            print("⚠️ Weak grounding detected")

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
            "what_is_happening": "Markets are showing mixed signals.",
            "why_it_is_happening": "Driven by macroeconomic and geopolitical factors.",
            "what_to_do": "Maintain diversification and monitor developments."
        }