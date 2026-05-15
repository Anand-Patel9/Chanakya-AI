# Dataset/asset_universe.py
import pandas as pd
from config import ASSET_METADATA_FILE

ASSET_UNIVERSE = {
    "equity_india": [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
        "HINDUNILVR.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "LT.NS",
        "KOTAKBANK.NS", "AXISBANK.NS", "ASIANPAINT.NS", "MARUTI.NS", "SUNPHARMA.NS",
        "BAJFINANCE.NS", "WIPRO.NS", "HCLTECH.NS", "ULTRACEMCO.NS", "TITAN.NS",
        "POWERGRID.NS", "NTPC.NS", "NESTLEIND.NS", "TECHM.NS", "ADANIPORTS.NS",
        "M&M.NS", "TATAMOTOR.NS", "JSWSTEEL.NS", "ONGC.NS", "COALINDIA.NS"
    ],
    "etf_india": [
        "NIFTYBEES.NS", "BANKBEES.NS", "GOLDBEES.NS", "JUNIORBEES.NS",
        "ITBEES.NS", "PHARMABEES.NS", "PSUBNKBEES.NS", "AUTOBEES.NS"
    ],
    "reit_invit": [
        "EMBASSY.NS", "MINDSPACE.NS", "BIRET.NS", "PGINVIT.NS", "INDIGRID.NS"
    ],
    "global_etf_proxy": [
        "SPY", "QQQ", "DIA", "IWM", "EFA",
        "EEM", "VNQ", "GLD", "SLV", "TLT",
        "LQD", "HYG", "XLE", "XLK", "XLF"
    ],
    "commodity_proxy": [
        "GLD", "SLV", "USO", "DBA", "CPER"
    ]
}

def build_asset_universe():
    rows = []

    for category, symbols in ASSET_UNIVERSE.items():
        for symbol in symbols:
            rows.append({
                "symbol": symbol,
                "category": category
            })

    df = pd.DataFrame(rows).drop_duplicates(subset=["symbol"]).reset_index(drop=True)
    df.to_csv(ASSET_METADATA_FILE, index=False)

    print(f"Asset universe saved to: {ASSET_METADATA_FILE}")
    print(f"Total unique assets: {len(df)}")
    print(df.groupby("category").size())

    return df

if __name__ == "__main__":
    build_asset_universe()