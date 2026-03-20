import pandas as pd
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

print("🚀 CHANAKYA PPO TRAINING - FINAL STABLE AMC VERSION")

# -------------------------------
# 1. LOAD DATA
# -------------------------------
df = pd.read_csv('chanakya_raw_data.csv', low_memory=False)

numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

print(f"📊 Loaded: {len(df):,} rows | {df['Symbol'].nunique()} stocks")

# -------------------------------
# 2. FILTER STOCKS
# -------------------------------
top_stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ITC.NS', 'SBIN.NS']
df = df[df['Symbol'].isin(top_stocks)].copy()

# -------------------------------
# 3. FEATURE ENGINEERING
# -------------------------------
print("🔧 Computing PPO features...")

df = df.sort_values(['Symbol', 'Date'])

df['Return'] = df.groupby('Symbol')['Close'].pct_change(fill_method=None).fillna(0)

df['Volatility'] = (
    df.groupby('Symbol')['Return']
    .rolling(20)
    .std()
    .reset_index(0, drop=True)
)

def safe_sharpe(x):
    return x.mean() / (x.std() + 1e-8) if len(x) > 5 else 0

df['Sharpe'] = (
    df.groupby('Symbol')['Return']
    .rolling(30)
    .apply(safe_sharpe)
    .reset_index(0, drop=True)
)

df['MA50'] = (
    df.groupby('Symbol')['Close']
    .rolling(50)
    .mean()
    .reset_index(0, drop=True)
)

df['MA_Signal'] = (df['Close'] > df['MA50']).astype(float)

df = df.fillna(0)

print(f"✅ PPO Ready: {len(df):,} rows")

# -------------------------------
# 4. PIVOT
# -------------------------------
pivot_returns = df.pivot(index='Date', columns='Symbol', values='Return').fillna(0)

print("Pivot shape:", pivot_returns.shape)

# -------------------------------
# 5. ENVIRONMENT
# -------------------------------
class ChanakyaPortfolioEnv(gym.Env):

    def __init__(self, returns_df):
        super().__init__()

        if len(returns_df) < 100:
            raise ValueError("❌ Not enough data")

        self.returns = returns_df
        self.n_assets = returns_df.shape[1]

        self.observation_space = spaces.Box(
            low=-5, high=5, shape=(5 + self.n_assets,), dtype=np.float32
        )

        self.action_space = spaces.Box(
            low=-2, high=2, shape=(self.n_assets,), dtype=np.float32
        )

        self.weights = np.ones(self.n_assets) / self.n_assets
        self.current_step = 50

    def reset(self, seed=None):
        self.current_step = np.random.randint(50, len(self.returns) - 50)
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

        # 🔥 SOFTMAX (no zero allocation)
        exp_weights = np.exp(action)
        weights = exp_weights / np.sum(exp_weights)

        # Smooth transitions
        weights = 0.9 * self.weights + 0.1 * weights

        returns = self.returns.iloc[self.current_step].values

        portfolio_return = np.dot(weights, returns)
        risk = np.std(returns)

        # ✅ Stable Sharpe reward
        reward = np.tanh(portfolio_return / (risk + 1e-8))

        # ✅ Moderate diversification
        reward -= 0.5 * np.sum(weights ** 2)

        # ✅ Max allocation constraint
        max_weight = np.max(weights)
        if max_weight > 0.4:
            reward -= 3 * (max_weight - 0.4)

        # ✅ Stability (reduce over-trading)
        change_penalty = np.sum(np.abs(weights - self.weights))
        reward -= 0.2 * change_penalty

        self.weights = weights
        self.current_step += 1

        terminated = self.current_step >= len(self.returns) - 1
        truncated = False

        return self._get_obs(), float(reward), terminated, truncated, {}

# -------------------------------
# 6. TRAIN MODEL
# -------------------------------
print("🎯 Training Chanakya Portfolio Agent...")

env = make_vec_env(lambda: ChanakyaPortfolioEnv(pivot_returns), n_envs=2)

model = PPO(
    policy="MlpPolicy",
    env=env,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    ent_coef=0.08,   # 🔥 exploration boost
    verbose=1
)

# 🔥 INCREASED TIMESTEPS
model.learn(total_timesteps=200000, progress_bar=True)

model.save("chanakya_portfolio_ppo_final")

print("✅ MODEL SAVED")

# -------------------------------
# 7. TEST MODEL
# -------------------------------
print("\n🧪 LIVE PORTFOLIO RECOMMENDATION:")

test_env = ChanakyaPortfolioEnv(pivot_returns)
obs, _ = test_env.reset()

action, _ = model.predict(obs, deterministic=True)

exp_weights = np.exp(action)
weights = exp_weights / np.sum(exp_weights)

for i, stock in enumerate(top_stocks):
    print(f"{stock}: {weights[i]:.2%}")