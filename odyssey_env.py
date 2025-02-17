from typing import Optional
import numpy as np
import gymnasium as gym
from odyssey_wrapper import OdysseyWrapper

imageWidth = 100
imageHeight = 100

class MarioOdysseyEnv(gym.Env):
    coinBonus = 50
    regionalCoinBonus = 70
    moonBonus = 100
    kingdomVisitedBonus = 1_000
    gameCompleteBonus = 1_000_000

    def __init__(self):
        # A Joy Stick has 2 Axis. We will use a nested action for a joystick
        # This nested action will have 2 indices, [0] representing horizontal
        # and [1] representing vertical. Each axis will have incremental values
        # ranging from -1 to 1 in steps of 0.2, making each axis have a total
        # of 11 possible options. 0 == -1, 1 == -0.8, 2 == -0.6, 3 == -0.4, 
        # 4 == -0.2, 5 == 0.0, 6 == 0.2, 7 == 0.4, 8 == 0.6, 9 == 0.8, 10 == 1.0
        # 
        # A button has 2 states, pressed and not-pressed. Therefore there will
        # 0 == not pressed and 1 == pressed
        # 
        # Action Space:
        # Left Joy Stick: [11, 11]
        # Jump Button: [2]
        # Crouch Button: [2]
        # Action Button: [2]
        # Release Cappy Button: [2]
        # Right Joy Stick: [11, 11]

        actionSpace = np.array([[11, 11], 2, 2, 2, 2, [11, 11]])
        self.action_space = gym.spaces.MultiDiscrete(actionSpace)

        # Observation space will include the 8 most recent frames
        observationSpace = {
            # The maximum number of coins in Super Mario Odyssey is 99,999
            "numCoins": gym.spaces.Box(0, 99_999),

            # The total number of regional coins across all kingdoms is 1,000
            "regionalCoins": gym.spaces.Box(0, 1_000),

            # The maximum number of moons a player can get is 999
            "moons": gym.spaces.Box(0, 999),

            # There are 17 kingdoms
            # See odyssey_kingdoms.py for a list of all of the kingdoms
            "kingdoms": gym.spaces.Box(0, 17),

            # Has cleared game
            "gameCleared": gym.spaces.Discrete(2),

            # The most recent frames
            "currentFrame": gym.spaces.Box(0, 255, (imageHeight, imageWidth, 3), dtype=np.uint8),
            "previousFrame1": gym.spaces.Box(0, 255, (imageHeight, imageWidth, 3), dtype=np.uint8),
            "previousFrame2": gym.spaces.Box(0, 255, (imageHeight, imageWidth, 3), dtype=np.uint8),
            "previousFrame3": gym.spaces.Box(0, 255, (imageHeight, imageWidth, 3), dtype=np.uint8),
            "previousFrame4": gym.spaces.Box(0, 255, (imageHeight, imageWidth, 3), dtype=np.uint8),
            "previousFrame5": gym.spaces.Box(0, 255, (imageHeight, imageWidth, 3), dtype=np.uint8),
            "previousFrame6": gym.spaces.Box(0, 255, (imageHeight, imageWidth, 3), dtype=np.uint8),
            "previousFrame7": gym.spaces.Box(0, 255, (imageHeight, imageWidth, 3), dtype=np.uint8),
        }

        self.observation_space = gym.spaces.Dict(observationSpace)

        self.odyssey_wrapper = OdysseyWrapper()

    
    def _get_observations(self):
        return self.odyssey_wrapper.get_observations()


    def _calculate_reward(self, observation):
        numCoins = observation["numCoins"]
        numRegionals = observation["regionalCoins"]
        numMoons = observation["moons"]
        visitedKingdoms = observation["kingdoms"]
        gameCleared = observation["gameCleared"]

        return (numCoins * self.coinBonus) + (numRegionals * self.regionalCoinBonus) + (numMoons * self.moonBonus) + (visitedKingdoms * self.kingdomVisitedBonus) + (self.gameCompleteBonus if gameCleared else 0)


    def _get_info(self):
        return self.odyssey_wrapper.get_info()


    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        self.odyssey_wrapper.reset()

        observation = self._get_observations()
        info = self._get_info()

        return observation, info
    

    def step(self, action):
        actionCommand = self.defineActionCommand(action)
        self.odyssey_wrapper.send_action(actionCommand)

        terminated = self.odyssey_wrapper.game_cleared
        truncated = False
        observation = self._get_observations()
        reward = self._calculate_reward(observation)
        info = self._get_info()
        return observation, reward, terminated, truncated, info


    def defineActionCommand(self, action):
        # Left Joy Stick: [11, 11]
        # Jump Button: [2]
        # Crouch Button: [2]
        # Action Button: [2]
        # Release Cappy Button: [2]
        # Right Joy Stick: [11, 11]  
        #       
        # Left Joystick to move
        # Right Joystick to control camera
        # A to jump
        # Y to action
        # ZR to crouch
        # ZL to release cappy

        commandBuilder = []

        leftJoystickAction = action[0]
        leftJoystickXAxis = leftJoystickAction[0]
        leftJoystickYAxis = leftJoystickAction[1]
        
        if leftJoystickXAxis < 5:
            commandBuilder.append("sb4")
        elif leftJoystickXAxis > 5:
            commandBuilder.append("sb2")
        
        if leftJoystickYAxis < 5:
            commandBuilder.append("sb3")
        elif leftJoystickYAxis > 5:
            commandBuilder.append("sb1")

        jump = action[1] == 1
        if jump:
            commandBuilder.append("a")

        crouch = action[2] == 1
        if crouch:
            commandBuilder.append("zr")

        actionButton = action[3] == 1
        if actionButton:
            commandBuilder.append("y")

        releaseCappy = action[4] == 1
        if releaseCappy:
            commandBuilder.append("zl")

        rightJoystickAction = action[0]
        rightJoystickXAxis = rightJoystickAction[0]
        rightJoystickYAxis = rightJoystickAction[1]

        if rightJoystickXAxis < 5:
            commandBuilder.append("sb8")
        elif rightJoystickXAxis > 5:
            commandBuilder.append("sb6")
        
        if rightJoystickYAxis < 5:
            commandBuilder.append("sb7")
        elif rightJoystickYAxis > 5:
            commandBuilder.append("sb5")

        return '+'.join(commandBuilder)

