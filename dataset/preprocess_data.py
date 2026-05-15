# Dataset/preprocess_data.py
import pandas as pd
import numpy as np
from pathlib import Path

from config import (
    RAW_DATA_FILE, MONTHLY_DATA_FILE,
    START_DATE, END_DATE, RISK_FREE_RATE
)


def load_raw_data():
    """Load raw data with proper dtype handling."""
    df = pd.read_csv(RAW_DATA_FILE, low_memory=False)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).reset_index(drop=True)
    return df


def clean_numeric_columns(df):
    """Convert price/volume columns to numeric, fill missing values."""
    price_cols = ["open", "high", "low", "close", "adj_close"]
    for col in price_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "volume" in df.columns:
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0)

    return df


def resample_to_monthly(df):
    """Convert daily data to monthly end-of-month data."""
    monthly = df.groupby(["symbol", pd.Grouper(key="date", freq="ME")]).agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "adj_close": "last",
        "volume": "sum"
    }).reset_index()

    monthly["date"] = pd.to_datetime(monthly["date"])
    return monthly


def add_monthly_returns(df):
    """Calculate monthly returns."""
    df = df.sort_values(["symbol", "date"])
    df["return"] = df.groupby("symbol")["adj_close"].pct_change()
    df["log_return"] = np.log(df["adj_close"] / df["adj_close"].shift(1))
    return df


def main():
    print("Loading raw data...")
    df = load_raw_data()
    print(f"Raw data shape: {df.shape}")

    print("Cleaning numeric columns...")
    df = clean_numeric_columns(df)
    print(f"After cleaning: {df.shape}")

    print("Resampling to monthly...")
    df_monthly = resample_to_monthly(df)
    print(f"Monthly shape: {df_monthly.shape}")

    print("Calculating returns...")
    df_monthly = add_monthly_returns(df_monthly)
    print(f"With returns: {df_monthly.shape}")

    # Final cleaning
    df_monthly = df_monthly.dropna(subset=["date", "close", "adj_close"])
    df_monthly = df_monthly[df_monthly["date"] >= pd.to_datetime(START_DATE)]
    df_monthly = df_monthly[df_monthly["date"] <= pd.to_datetime(END_DATE)]

    df_monthly.to_csv(MONTHLY_DATA_FILE, index=False)
    
    print("\nMonthly preprocessing completed!")
    print(f"Final monthly dataset: {len(df_monthly)} rows, {df_monthly['symbol'].nunique()} symbols")
    print(f"Date range: {df_monthly['date'].min()} to {df_monthly['date'].max()}")
    print(f"File saved: {MONTHLY_DATA_FILE}")
    print("\nColumns:", list(df_monthly.columns))
    print("Next: build_features.py for PPO state features")


if __name__ == "__main__":
    main()