import requests


def fetch_market_data():

    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%5ENSEI,%5EBSESN"

    r = requests.get(url).json()

    result = r["quoteResponse"]["result"]

    data = []

    for index in result:

        data.append({
            "symbol": index["symbol"],
            "price": index["regularMarketPrice"],
            "change": index["regularMarketChangePercent"]
        })

    return data