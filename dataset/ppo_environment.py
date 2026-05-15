# Dataset/ppo_environment.py
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd
import config


class PortfolioEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self):
        super().__init__()

        self.data = pd.read_csv(config.FEATURES_FILE)
        self.data["date"] = pd.to_datetime(self.data["date"])
        self.data = self.data.sort_values(["date", "symbol"]).reset_index(drop=True)

        self.feature_cols = [
            "vol_3m", "vol_6m", "mom_1m", "mom_3m",
            "mom_6m", "mom_12m", "sharpe_6m", "range_pos_6m", "regime"
        ]

        self.assets = sorted(self.data["symbol"].unique())
        self.dates = sorted(self.data["date"].unique())

        self.n_assets = len(self.assets)
        self.n_features = len(self.feature_cols)
        self.n_timesteps = len(self.dates)

        self.observation_space = spaces.Box(
            low=-10.0,
            high=10.0,
            shape=(self.n_assets * self.n_features,),
            dtype=np.float32
        )

        self.action_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(self.n_assets,),
            dtype=np.float32
        )

        self.current_step = 0
        self.portfolio_value = 1.0
        self.portfolio_returns = []

    def _get_step_data(self):
        current_date = self.dates[self.current_step]
        step_data = self.data[self.data["date"] == current_date].copy()
        step_data = step_data.set_index("symbol").reindex(self.assets).reset_index()
        return step_data

    def _get_observation(self):
        step_data = self._get_step_data()
        obs = step_data[self.feature_cols].fillna(0.0).to_numpy(dtype=np.float32)
        obs = np.nan_to_num(obs, nan=0.0, posinf=0.0, neginf=0.0)
        return obs.flatten()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 12
        self.portfolio_value = 1.0
        self.portfolio_returns = []
        observation = self._get_observation()
        info = {}
        return observation, info

    def step(self, action):
        action = np.asarray(action, dtype=np.float32)
        action = np.clip(action, 0.0, 1.0)

        if np.sum(action) <= 1e-8:
            action = np.ones(self.n_assets, dtype=np.float32) / self.n_assets
        else:
            action = action / np.sum(action)

        step_data = self._get_step_data()

        asset_returns = step_data["return"].fillna(0.0).to_numpy(dtype=np.float32)
        asset_returns = np.nan_to_num(asset_returns, nan=0.0, posinf=0.0, neginf=0.0)

        # Safety clipping for impossible/corrupted monthly values
        asset_returns = np.clip(asset_returns, -0.30, 0.30)

        portfolio_return = float(np.dot(action, asset_returns))
        portfolio_return = float(np.nan_to_num(portfolio_return, nan=0.0, posinf=0.0, neginf=0.0))

        self.portfolio_value *= (1.0 + portfolio_return)
        self.portfolio_value = float(np.nan_to_num(self.portfolio_value, nan=1.0, posinf=1.0, neginf=1.0))

        self.portfolio_returns.append(portfolio_return)

        if len(self.portfolio_returns) >= 6:
            recent_returns = np.array(self.portfolio_returns[-6:], dtype=np.float32)
            std = np.std(recent_returns)
            reward = float(np.mean(recent_returns) / (std + 1e-8) * np.sqrt(12))
        else:
            reward = portfolio_return

        reward = float(np.nan_to_num(reward, nan=0.0, posinf=0.0, neginf=0.0))

        self.current_step += 1
        terminated = self.current_step >= self.n_timesteps
        truncated = False

        if terminated:
            next_obs = np.zeros(self.n_assets * self.n_features, dtype=np.float32)
        else:
            next_obs = self._get_observation()

        info = {
            "portfolio_value": self.portfolio_value,
            "portfolio_return": portfolio_return,
            "reward": reward
        }

        return next_obs, reward, terminated, truncated, info