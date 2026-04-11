import os
from groq import Groq

# Initialize client safely
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def summarize(text: str):
    """
    Summarizes financial news into 2–3 lines.
    Includes error handling to prevent API crashes.
    """

    # ✅ Handle empty input
    if not text or not text.strip():
        return "No content available to summarize."

    prompt = f"""
Summarize the following financial news in 2-3 lines.
Focus on market impact and key insight.

{text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ WORKING MODEL
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ Summarizer Error:", str(e))

        # ✅ Graceful fallback (VERY IMPORTANT)
        return "Summary unavailable due to model/API issue."