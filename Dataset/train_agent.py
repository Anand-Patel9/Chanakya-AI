import pandas as pd
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

print("🚀 CHANAKYA PPO TRAINING - ERROR FREE")

# 1. LOAD & CLEAN YOUR DATASET
df = pd.read_csv('chanakya_raw_data.csv', low_memory=False)

# ✅ FIX: Force numeric columns (handles string issues)
numeric_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

print(f"📊 Loaded: {len(df):,} rows | {df['Symbol'].nunique()} stocks")

# 2. BULLETPROOF FEATURE ENGINEERING
print("🔧 Computing PPO features...")
for symbol in df['Symbol'].unique()[:20]:  # Limit to 20 stocks for speed
    mask = df['Symbol'] == symbol
    symbol_data = df.loc[mask, ['Close']].copy()
    
    # Safe returns calculation
    symbol_data['Return'] = symbol_data['Close'].pct_change().fillna(0)
    df.loc[mask, 'Return'] = symbol_data['Return'].values
    
    # Safe volatility
    symbol_data['Volatility'] = symbol_data['Return'].rolling(20, min_periods=5).std().fillna(0.02)
    df.loc[mask, 'Volatility'] = symbol_data['Volatility'].values
    
    # Safe MA signal
    ma50 = symbol_data['Close'].rolling(50, min_periods=10).mean()
    df.loc[mask, 'MA_Signal'] = (symbol_data['Close'] > ma50).astype(float).values
    
    # Safe Sharpe
    def safe_sharpe(x):
        return x.mean() / (x.std() + 1e-8) if len(x) > 5 and x.std() > 0 else 0
    
    symbol_data['Sharpe'] = symbol_data['Return'].rolling(30, min_periods=10).apply(safe_sharpe)
    df.loc[mask, 'Sharpe'] = symbol_data['Sharpe'].values

# Clean final dataset
df = df.dropna(subset=['Return', 'Volatility', 'Sharpe', 'Volume']).reset_index(drop=True)
print(f"✅ PPO Ready: {len(df):,} rows | Features OK")

# 3. PPO ENVIRONMENT
class ChanakyaPortfolioEnv(gym.Env):
    def __init__(self, df):
        super().__init__()
        self.df = df.reset_index(drop=True)
        self.current_step = 0
        
        self.observation_space = spaces.Box(low=-2, high=2, shape=(5,), dtype=np.float32)
        self.action_space = spaces.Box(low=0, high=1, shape=(6,), dtype=np.float32)
    
    def reset(self, seed=None):
        self.current_step = np.random.randint(50, len(self.df)-50)
        return self._get_obs(), {}
    
    def _get_obs(self):
        row = self.df.iloc[self.current_step]
        return np.array([
            float(row['Return']),
            float(row['Volatility']),
            float(row['Sharpe']),
            float(row['MA_Signal']),
            float(np.log(row['Volume'] + 1) / 20)
        ], dtype=np.float32)
    
    def step(self, action):
        action = action / (np.sum(action) + 1e-8)  # Normalize weights
        
        reward = float(self.df.iloc[self.current_step]['Sharpe'])
        reward -= 0.3 * float(self.df.iloc[self.current_step]['Volatility'])  # Risk penalty
        
        self.current_step += 1
        terminated = self.current_step >= len(self.df) - 10
        truncated = False
        
        return self._get_obs(), reward, terminated, truncated, {}

# 4. TRAIN PPO
print("🎯 Training Chanakya Portfolio Agent...")
env = make_vec_env(lambda: ChanakyaPortfolioEnv(df), n_envs=2)

model = PPO(
    policy="MlpPolicy",
    env=env,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    verbose=1
)

model.learn(total_timesteps=50000, progress_bar=True)
model.save("chanakya_portfolio_ppo_final")

print("✅ SAVED: chanakya_portfolio_ppo_final.zip")

# 5. TEST
print("\n🧪 LIVE PORTFOLIO RECOMMENDATION:")
test_env = ChanakyaPortfolioEnv(df)
obs, _ = test_env.reset()
action, _ = model.predict(obs, deterministic=True)

weights = action[0] / np.sum(action[0])
top_stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ITC.NS', 'SBIN.NS']
print("Top 3 allocations:")
for i, w in enumerate(weights[:3]):
    print(f"  {top_stocks[i]}: {w:.1%}")