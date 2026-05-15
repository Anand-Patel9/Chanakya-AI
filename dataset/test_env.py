import numpy as np
from ppo_environment import PortfolioEnv

env = PortfolioEnv()
obs, info = env.reset()

print(f"State shape: {obs.shape}")

action = np.ones(env.n_assets, dtype=np.float32) / env.n_assets
obs, reward, done, truncated, info = env.step(action)

print(f"Action shape: {action.shape}")
print(f"Portfolio value: {info.get('portfolio_value', 0):.4f}")
print(f"Portfolio return: {info.get('portfolio_return', 0):.6f}")
print(f"Reward: {info.get('reward', 0):.6f}")