# Dataset/train_ppo.py
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv
from ppo_environment import PortfolioEnv


def make_env():
    return PortfolioEnv()


def main():
    env = PortfolioEnv()
    check_env(env, warn=True)

    vec_env = DummyVecEnv([make_env])

    model = PPO(
        policy="MlpPolicy",
        env=vec_env,
        learning_rate=3e-4,
        n_steps=128,
        batch_size=32,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
        vf_coef=0.5,
        max_grad_norm=0.5,
        verbose=1,
        tensorboard_log="./ppo_logs/"
    )

    print("Starting PPO training...")
    model.learn(total_timesteps=20000)

    model.save("ppo_portfolio_strategy")
    print("Model saved as ppo_portfolio_strategy.zip")

    test_env = PortfolioEnv()
    obs, _ = test_env.reset()
    terminated = False
    truncated = False

    while not (terminated or truncated):
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = test_env.step(action)

    print(f"Final portfolio value: {info['portfolio_value']:.4f}")
    print(f"Final portfolio return: {info['portfolio_return']:.6f}")
    print(f"Final reward: {info['reward']:.6f}")


if __name__ == "__main__":
    main()