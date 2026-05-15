# Dataset/config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"
METADATA_DIR = BASE_DIR / "metadata"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)

START_DATE = "2016-01-01"
END_DATE = "2026-01-01"

REBALANCE_FREQUENCY = "M"
RISK_FREE_RATE = 0.06

RAW_DATA_FILE = RAW_DIR / "market_data_raw.csv"
MONTHLY_DATA_FILE = PROCESSED_DIR / "market_data_monthly.csv"
FEATURE_DATA_FILE = PROCESSED_DIR / "portfolio_features.csv"
ASSET_METADATA_FILE = METADATA_DIR / "asset_universe.csv"
FEATURES_FILE = PROCESSED_DIR / "market_data_features.csv"