# Dataset/evaluate_ppo.py
import numpy as np
import pandas as pd
from stable_baselines3 import PPO
from ppo_environment import PortfolioEnv


MODEL_PATH = "ppo_portfolio_strategy.zip"


def compute_metrics(values, returns, periods_per_year=12):
    values = np.array(values, dtype=np.float64)
    returns = np.array(returns, dtype=np.float64)

    total_return = values[-1] / values[0] - 1 if len(values) > 1 else 0.0
    n_periods = len(returns)

    if n_periods > 0:
        cagr = (values[-1] / values[0]) ** (periods_per_year / n_periods) - 1
        volatility = np.std(returns) * np.sqrt(periods_per_year)
        sharpe = (np.mean(returns) / (np.std(returns) + 1e-8)) * np.sqrt(periods_per_year)
    else:
        cagr = 0.0
        volatility = 0.0
        sharpe = 0.0

    running_max = np.maximum.accumulate(values)
    drawdowns = (values - running_max) / running_max
    max_drawdown = np.min(drawdowns) if len(drawdowns) > 0 else 0.0

    return {
        "Total Return": total_return,
        "CAGR": cagr,
        "Volatility": volatility,
        "Sharpe": sharpe,
        "Max Drawdown": max_drawdown
    }


def main():
    env = PortfolioEnv()
    model = PPO.load(MODEL_PATH)

    obs, _ = env.reset()
    terminated = False
    truncated = False

    portfolio_values = [env.portfolio_value]
    portfolio_returns = []
    rewards = []

    step_records = []

    while not (terminated or truncated):
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)

        portfolio_value = info["portfolio_value"]
        portfolio_return = info["portfolio_return"]

        portfolio_values.append(portfolio_value)
        portfolio_returns.append(portfolio_return)
        rewards.append(reward)

        current_date = env.dates[min(env.current_step - 1, len(env.dates) - 1)]

        step_records.append({
            "date": current_date,
            "portfolio_value": portfolio_value,
            "portfolio_return": portfolio_return,
            "reward": reward
        })

    metrics = compute_metrics(portfolio_values, portfolio_returns)

    print("\n=== PPO Portfolio Evaluation ===")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")

    print(f"Final Portfolio Value: {portfolio_values[-1]:.4f}")
    print(f"Average Reward: {np.mean(rewards):.4f}")

    results_df = pd.DataFrame(step_records)
    metrics_df = pd.DataFrame([metrics])

    results_df.to_csv("ppo_evaluation_timeseries.csv", index=False)
    metrics_df.to_csv("ppo_evaluation_metrics.csv", index=False)

    print("\nSaved:")
    print("- ppo_evaluation_timeseries.csv")
    print("- ppo_evaluation_metrics.csv")


if __name__ == "__main__":
    main()