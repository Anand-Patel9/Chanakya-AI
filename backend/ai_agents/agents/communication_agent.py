import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_response(state):

    research = state.get("research_data", {})
    risk = state.get("risk_data", {})

    prompt = f"""
You are an AI financial analyst.

Use the following data to generate a clear, professional market insight.

Research Data:
{research}

Risk Data:
{risk}

Generate:
1. Market summary
2. Risk analysis
3. Actionable insight
4. Recommendation

Keep it concise and professional.
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()