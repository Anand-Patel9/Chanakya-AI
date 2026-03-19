import random

def run_communication_agent(question: str):

    responses = {
        "invest": "Technology and AI sectors currently show strong growth potential based on recent market intelligence.",
        "risk": "Current portfolio risk remains moderate. Diversification across sectors is recommended.",
        "market": "Market sentiment appears neutral with moderate volatility expected in the coming weeks.",
        "portfolio": "A balanced portfolio across technology, healthcare, and finance can improve stability."
    }

    question_lower = question.lower()

    for key in responses:
        if key in question_lower:
            return {
                "answer": responses[key],
                "confidence": round(random.uniform(0.75, 0.95), 2)
            }

    return {
        "answer": "Based on current market analysis, diversified investment across stable sectors is recommended.",
        "confidence": 0.75
    }