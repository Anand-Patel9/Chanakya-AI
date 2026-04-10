import os
from typing import Dict, Any
from groq import Groq


def run_communication_agent(
    question: str,
    research_data: Dict[str, Any] = None,
    risk_data: Dict[str, Any] = None
) -> Dict[str, str]:
    """
    Communication Agent
    - Generates final AI response using Groq LLM
    - Combines research + risk insights
    """

    try:
        # ✅ Initialize Groq INSIDE function (important fix)
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        # ✅ Safety fallback (if orchestrator doesn't pass data)
        research_data = research_data or {}
        risk_data = risk_data or {}

        # ✅ Prompt Engineering (clean + structured)
        prompt = f"""
You are an expert AI financial analyst.

User Question:
{question}

Research Insights:
{research_data}

Risk Analysis:
{risk_data}

Provide a structured response with:

1. Market Summary
2. Risk Evaluation
3. Key Insights
4. Final Recommendation

Keep it concise, professional, and actionable.
"""

        # ✅ Call Groq API
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        output = response.choices[0].message.content.strip()

        return {
            "response": output
        }

    except Exception as e:
        # ❌ Proper error handling (no crash)
        return {
            "response": f"Communication Agent Error: {str(e)}"
        }