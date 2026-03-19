import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def summarize(text):

    prompt = f"""
Summarize the following financial news in 2-3 lines.
Focus on market impact and key insight.

{text}
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()