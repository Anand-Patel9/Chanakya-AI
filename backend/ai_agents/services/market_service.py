import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_market_data(symbol="AAPL"):  # ✅ default fallback

    print("🔥 FINNHUB FUNCTION EXECUTED")
    try:
        api_key = os.getenv("FINNHUB_API_KEY")

        if not api_key:
            return {"error": "FINNHUB_API_KEY not found"}

        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return {"error": f"API failed: {response.status_code}"}

        data = response.json()

        return {
            "symbol": symbol,
            "current_price": data.get("c"),
            "high": data.get("h"),
            "low": data.get("l"),
            "open": data.get("o"),
            "previous_close": data.get("pc")
        }

    except Exception as e:
        return {"error": str(e)}