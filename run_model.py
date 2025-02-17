import os
import gymnasium as gym
from stable_baselines3 import PPO

models_dir = "models/PPO"

env = gym.make("MarioOdysseyEnv-v0")
env.reset()

logsdir = "logs"
if not os.path.exists(logsdir):
    os.makedirs(logsdir)

ideal_model = ""
model_path = f"{models_dir}/{ideal_model}"
model = PPO.load(model_path, env=env, tensorboard_log=logsdir)

observation, info = env.reset()
done = observation["gameCleared"] == True

while not done:
    action, _states = model.predict(observation)
    observation, rewards, done, info = env.step(action)
    print(rewards)