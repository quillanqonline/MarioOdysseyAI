from gymnasium.envs.registration import register
from envs.odyssey_env import MarioOdysseyEnv

register(
    id="MarioOdysseyEnv-v0",
    entry_point="envs:MarioOdysseyEnv",
)