import pandas as pd
import numpy as np
import config

def load_monthly_data():
    df = pd.read_csv(config.MONTHLY_DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["symbol", "date"]).reset_index(drop=True)
    return df

def add_rolling_features(df):
    feature_cols = []

    df["vol_3m"] = (
        df.groupby("symbol")["log_return"]
        .rolling(3, min_periods=2)
        .std()
        .reset_index(level=0, drop=True)
    )
    feature_cols.append("vol_3m")

    df["vol_6m"] = (
        df.groupby("symbol")["log_return"]
        .rolling(6, min_periods=3)
        .std()
        .reset_index(level=0, drop=True)
    )
    feature_cols.append("vol_6m")

    df["mom_1m"] = df.groupby("symbol")["adj_close"].pct_change(1)
    df["mom_3m"] = df.groupby("symbol")["adj_close"].pct_change(3)
    df["mom_6m"] = df.groupby("symbol")["adj_close"].pct_change(6)
    df["mom_12m"] = df.groupby("symbol")["adj_close"].pct_change(12)
    feature_cols.extend(["mom_1m", "mom_3m", "mom_6m", "mom_12m"])

    rolling_mean_6 = (
        df.groupby("symbol")["log_return"]
        .rolling(6, min_periods=3)
        .mean()
        .reset_index(level=0, drop=True)
    )
    rolling_std_6 = (
        df.groupby("symbol")["log_return"]
        .rolling(6, min_periods=3)
        .std()
        .reset_index(level=0, drop=True)
    )
    df["sharpe_6m"] = rolling_mean_6 / rolling_std_6.replace(0, np.nan)
    feature_cols.append("sharpe_6m")

    rolling_low_6 = (
        df.groupby("symbol")["low"]
        .rolling(6, min_periods=3)
        .min()
        .reset_index(level=0, drop=True)
    )
    rolling_high_6 = (
        df.groupby("symbol")["high"]
        .rolling(6, min_periods=3)
        .max()
        .reset_index(level=0, drop=True)
    )
    df["range_pos_6m"] = (df["close"] - rolling_low_6) / (rolling_high_6 - rolling_low_6).replace(0, np.nan)
    feature_cols.append("range_pos_6m")

    return df, feature_cols

def add_market_regime_features(df):
    df["regime"] = np.where(df["mom_6m"] > 0.10, 1, np.where(df["mom_6m"] < -0.10, -1, 0))
    return df

def main():
    print("Loading monthly data...")
    df = load_monthly_data()
    print(f"Monthly shape: {df.shape}")

    print("Adding rolling features...")
    df, feature_cols = add_rolling_features(df)

    print("Adding regime features...")
    df = add_market_regime_features(df)

    df = df[(df["date"] >= pd.to_datetime(config.START_DATE)) & (df["date"] <= pd.to_datetime(config.END_DATE))]

    fill_cols = feature_cols + ["regime"]
    df[fill_cols] = df.groupby("symbol")[fill_cols].ffill().fillna(0)

    df.to_csv(config.FEATURES_FILE, index=False)

    print("\\nPPO features completed!")
    print(f"Final dataset: {len(df)} rows, {df['symbol'].nunique()} symbols")
    print(f"Feature columns: {feature_cols + ['regime']}")
    print(f"File saved: {config.FEATURES_FILE}")

if __name__ == "__main__":
    main()