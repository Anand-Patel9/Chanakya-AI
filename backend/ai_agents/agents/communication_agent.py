import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_communication_agent(query, research_data, risk_data):

    prompt = f"""
You are an AI financial analyst.

User Query:
{query}

Research Data:
{research_data}

Risk Data:
{risk_data}

Generate:
1. Market summary
2. Risk analysis
3. Actionable insight
4. Recommendation

Keep it concise and professional.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ FIXED MODEL
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Communication Agent Error: {str(e)}"