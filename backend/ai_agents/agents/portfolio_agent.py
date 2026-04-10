import numpy as np
import os
from stable_baselines3 import PPO
import pandas as pd
import gymnasium as gym
from gymnasium import spaces

# -------------------------------
# PATH SETUP
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "../../Dataset")

MODEL_PATH = os.path.join(DATASET_PATH, "chanakya_portfolio_ppo_final.zip")
DATA_PATH = os.path.join(DATASET_PATH, "chanakya_raw_data.csv")

# -------------------------------
# SAFE MODEL LOADING
# -------------------------------
model = None

def load_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise Exception(f"Model not found at {MODEL_PATH}")
        model = PPO.load(MODEL_PATH)
    return model


# -------------------------------
# LOAD & PREP DATA
# -------------------------------
df = pd.read_csv(DATA_PATH)

top_stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ITC.NS', 'SBIN.NS']
df = df[df['Symbol'].isin(top_stocks)].copy()

df = df.sort_values(['Symbol', 'Date'])
df['Return'] = df.groupby('Symbol')['Close'].pct_change().fillna(0)

pivot_returns = df.pivot(index='Date', columns='Symbol', values='Return').fillna(0)


# -------------------------------
# ENVIRONMENT
# -------------------------------
class ChanakyaPortfolioEnv(gym.Env):

    def __init__(self, returns_df):
        super().__init__()
        self.returns = returns_df
        self.n_assets = returns_df.shape[1]
        self.current_step = 50

        self.observation_space = spaces.Box(
            low=-5, high=5, shape=(5 + self.n_assets,), dtype=np.float32
        )

        self.action_space = spaces.Box(
            low=0, high=1, shape=(self.n_assets,), dtype=np.float32
        )

        self.weights = np.ones(self.n_assets) / self.n_assets

    def reset(self, seed=None):
        self.current_step = 50
        self.weights = np.ones(self.n_assets) / self.n_assets
        return self._get_obs(), {}

    def _get_obs(self):
        returns_row = self.returns.iloc[self.current_step]

        features = np.array([
            np.mean(returns_row),
            np.std(returns_row),
            np.max(returns_row),
            np.min(returns_row),
            np.sum(returns_row)
        ], dtype=np.float32)

        return np.concatenate([features, self.weights])

    def step(self, action):
        weights = action / (np.sum(action) + 1e-8)
        returns = self.returns.iloc[self.current_step].values

        portfolio_return = np.dot(weights, returns)
        risk = np.std(returns)

        reward = portfolio_return / (risk + 1e-8)

        self.weights = weights
        self.current_step += 1

        terminated = self.current_step >= len(self.returns) - 1
        truncated = False

        return self._get_obs(), float(reward), terminated, truncated, {}


# -------------------------------
# MAIN FUNCTION
# -------------------------------
def run_portfolio_agent():
    try:
        model = load_model()

        env = ChanakyaPortfolioEnv(pivot_returns)
        obs, _ = env.reset()

        action, _ = model.predict(obs, deterministic=True)

        # ✅ Softmax (better than raw normalization)
        exp_weights = np.exp(action)
        weights = exp_weights / np.sum(exp_weights)

        return {
            "portfolio": dict(zip(top_stocks, weights.tolist()))
        }

    except Exception as e:
        return {
            "error": "Portfolio Agent Failed",
            "details": str(e)
        }