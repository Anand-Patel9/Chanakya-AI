# Dataset/download_data.py
import time
import pandas as pd
import yfinance as yf

from config import START_DATE, END_DATE, RAW_DATA_FILE, ASSET_METADATA_FILE


def flatten_columns(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            "_".join([str(part) for part in col if str(part) != ""])
            for col in df.columns.to_flat_index()
        ]
    else:
        df.columns = [str(col) for col in df.columns]
    return df


def normalize_columns(df):
    df = flatten_columns(df)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df


def standardize_price_columns(df):
    column_map = {}

    for col in df.columns:
        if col.startswith("open"):
            column_map[col] = "open"
        elif col.startswith("high"):
            column_map[col] = "high"
        elif col.startswith("low"):
            column_map[col] = "low"
        elif col.startswith("close") and "adj" not in col:
            column_map[col] = "close"
        elif "adj" in col and "close" in col:
            column_map[col] = "adj_close"
        elif col.startswith("volume"):
            column_map[col] = "volume"
        elif col in ["date", "datetime", "index"]:
            column_map[col] = "date"

    df = df.rename(columns=column_map)
    return df


def download_symbol_data(symbol):
    try:
        df = yf.download(
            symbol,
            start=START_DATE,
            end=END_DATE,
            auto_adjust=False,
            progress=False
        )

        if df is None or df.empty:
            print(f"Skipping {symbol}: no data returned")
            return None

        df = df.reset_index()
        df = normalize_columns(df)
        df = standardize_price_columns(df)

        if "date" not in df.columns:
            print(f"Skipping {symbol}: date column missing after reset_index")
            return None

        for col in ["open", "high", "low", "close", "volume"]:
            if col not in df.columns:
                df[col] = pd.NA

        if "adj_close" not in df.columns:
            df["adj_close"] = df["close"]

        df = df[["date", "open", "high", "low", "close", "adj_close", "volume"]].copy()
        df["symbol"] = symbol
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"]).reset_index(drop=True)

        return df

    except Exception as e:
        print(f"Error downloading {symbol}: {e}")
        return None


def main():
    asset_df = pd.read_csv(ASSET_METADATA_FILE)
    symbols = asset_df["symbol"].dropna().unique().tolist()

    all_data = []
    success_count = 0
    fail_count = 0

    print(f"Starting download for {len(symbols)} assets...")
    print(f"Date range: {START_DATE} to {END_DATE}")

    for i, symbol in enumerate(symbols, start=1):
        print(f"[{i}/{len(symbols)}] Downloading {symbol}...")

        df = download_symbol_data(symbol)

        if df is not None and not df.empty:
            all_data.append(df)
            success_count += 1
            print(f"   Success: {len(df)} rows")
        else:
            fail_count += 1
            print("   Failed")

        time.sleep(0.5)

    if not all_data:
        print("No data downloaded.")
        return

    final_df = pd.concat(all_data, ignore_index=True)
    final_df = final_df.sort_values(["symbol", "date"]).reset_index(drop=True)
    final_df.to_csv(RAW_DATA_FILE, index=False)

    print("\nDownload completed.")
    print(f"Successful assets: {success_count}")
    print(f"Failed assets: {fail_count}")
    print(f"Total rows saved: {len(final_df)}")
    print(f"Unique symbols: {final_df['symbol'].nunique()}")
    print(f"Raw dataset saved to: {RAW_DATA_FILE}")


if __name__ == "__main__":
    main()