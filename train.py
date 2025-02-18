import gymnasium
from envs.odyssey_env import MarioOdysseyEnv
from stable_baselines3 import PPO
import os

models_dir = "models/PPO"
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

logsdir = "logs"
if not os.path.exists(logsdir):
    os.makedirs(logsdir)

env = gymnasium.make("MarioOdysseyEnv-v0")

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logsdir)

TIMESTEPS = 100_000
iterations = 0
while True:
    env.reset()
    iterations += 1
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=True, tb_log_name="PPO")
    model.save(f"{models_dir}/{iterations}")
