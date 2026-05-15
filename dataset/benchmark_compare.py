import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
        positive_months = float((returns > 0).mean())
    else:
        cagr = 0.0
        volatility = 0.0
        sharpe = 0.0
        positive_months = 0.0

    running_max = np.maximum.accumulate(values)
    drawdowns = (values - running_max) / running_max
    max_drawdown = np.min(drawdowns) if len(drawdowns) > 0 else 0.0

    return {
        "Total Return": total_return,
        "CAGR": cagr,
        "Volatility": volatility,
        "Sharpe": sharpe,
        "Max Drawdown": max_drawdown,
        "Positive Months": positive_months,
        "Final Portfolio Value": values[-1] if len(values) > 0 else 1.0
    }


def run_ppo_strategy():
    env = PortfolioEnv()
    model = PPO.load(MODEL_PATH)

    obs, _ = env.reset()
    terminated = False
    truncated = False

    portfolio_values = [env.portfolio_value]
    portfolio_returns = []
    records = []

    while not (terminated or truncated):
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)

        current_date = env.dates[min(env.current_step - 1, len(env.dates) - 1)]

        records.append({
            "date": current_date,
            "strategy": "PPO",
            "portfolio_value": info["portfolio_value"],
            "portfolio_return": info["portfolio_return"],
            "reward": reward
        })

        portfolio_values.append(info["portfolio_value"])
        portfolio_returns.append(info["portfolio_return"])

    return pd.DataFrame(records), compute_metrics(portfolio_values, portfolio_returns)


def run_equal_weight_strategy():
    env = PortfolioEnv()

    obs, _ = env.reset()
    terminated = False
    truncated = False

    portfolio_values = [env.portfolio_value]
    portfolio_returns = []
    records = []

    equal_weight_action = np.ones(env.n_assets, dtype=np.float32) / env.n_assets

    while not (terminated or truncated):
        obs, reward, terminated, truncated, info = env.step(equal_weight_action)

        current_date = env.dates[min(env.current_step - 1, len(env.dates) - 1)]

        records.append({
            "date": current_date,
            "strategy": "Equal Weight",
            "portfolio_value": info["portfolio_value"],
            "portfolio_return": info["portfolio_return"],
            "reward": reward
        })

        portfolio_values.append(info["portfolio_value"])
        portfolio_returns.append(info["portfolio_return"])

    return pd.DataFrame(records), compute_metrics(portfolio_values, portfolio_returns)


def save_equity_curve(combined_df):
    combined_df["date"] = pd.to_datetime(combined_df["date"])
    pivot_df = combined_df.pivot(index="date", columns="strategy", values="portfolio_value").sort_index()

    plt.figure(figsize=(12, 6))
    for strategy in pivot_df.columns:
        plt.plot(pivot_df.index, pivot_df[strategy], label=strategy, linewidth=2)

    plt.title("Equity Curve: PPO vs Equal Weight")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("equity_curve.png", dpi=300)
    plt.close()


def main():
    ppo_df, ppo_metrics = run_ppo_strategy()
    ew_df, ew_metrics = run_equal_weight_strategy()

    combined_df = pd.concat([ppo_df, ew_df], ignore_index=True)

    metrics_df = pd.DataFrame([
        {"Strategy": "PPO", **ppo_metrics},
        {"Strategy": "Equal Weight", **ew_metrics}
    ])

    combined_df.to_csv("benchmark_comparison_timeseries.csv", index=False)
    metrics_df.to_csv("benchmark_comparison_metrics.csv", index=False)

    save_equity_curve(combined_df)

    print("\n=== Benchmark Comparison ===")
    print(metrics_df.to_string(index=False))
    print("\nSaved files:")
    print("- benchmark_comparison_timeseries.csv")
    print("- benchmark_comparison_metrics.csv")
    print("- equity_curve.png")


if __name__ == "__main__":
    main()