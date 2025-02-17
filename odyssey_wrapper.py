from odyssey_kingdoms import MarioOdysseyKingdoms
from file_manager import ScreenshotManager
from actionHandling.socket_server import SocketServer
import asyncio

class OdysseyWrapper:
    _fps = 60
    coin_count = 0
    moon_count = 0
    regional_coins = {}
    visited_kingdoms = 1
    current_kingdom = MarioOdysseyKingdoms.CAP
    taking_screenshots = False
    game_cleared = False
    socketServer: SocketServer = None

    def __init__(self):
        self.start_action_server()
        self.reset()


    def reset(self):
        self.taking_screenshots = False
        self.regional_coins = { MarioOdysseyKingdoms.CAP: 0 }
        self.visited_kingdoms = 1
        self.coin_count = 0
        self.moon_count = 0
        self.game_cleared = False
        self.current_kingdom = MarioOdysseyKingdoms.CAP
        _ = input("Press enter when the Mario Odyssey game has started a new game file...")
        self.taking_screenshots = True
        asyncio.run(self.take_screenshots())
    

    async def take_screenshots(self):
        while self.taking_screenshots:
            await asyncio.sleep(1 / self.fps)
            ScreenshotManager.updateScreenshots()
            self.update_state()


    def update_state(self):
        # TODO: Using the most recent screenshot, update currently saved values
        pass

    def get_observations(self):
        return {
            "numCoins": self.coin_count,
            "regionalCoins": self.calculate_collected_regional_coins(),
            "moons": self.moon_count,
            "kingdoms": self.visited_kingdoms,
            "gameCleared": self.game_cleared,
            "currentFrame": ScreenshotManager.get_image(ScreenshotManager.current_screenshot_title),
            "previousFrame1": ScreenshotManager.get_image(ScreenshotManager.get_previous_image_name(1)),
            "previousFrame2": ScreenshotManager.get_image(ScreenshotManager.get_previous_image_name(2)),
            "previousFrame3": ScreenshotManager.get_image(ScreenshotManager.get_previous_image_name(3)),
            "previousFrame4": ScreenshotManager.get_image(ScreenshotManager.get_previous_image_name(4)),
            "previousFrame5": ScreenshotManager.get_image(ScreenshotManager.get_previous_image_name(5)),
            "previousFrame6": ScreenshotManager.get_image(ScreenshotManager.get_previous_image_name(6)),
            "previousFrame7": ScreenshotManager.get_image(ScreenshotManager.get_previous_image_name(7))
        }
    
    
    def get_info(self):
        return {
            "takingScreenshots": self.taking_screenshots,
            "currentKingdom": self.current_kingdom,
            "regionalCoins": self.regional_coins
        }
    

    def calculate_collected_regional_coins(self):
        return sum(self.regional_coins.values())
    

    def start_action_server(self):
        self.socketServer = SocketServer()
        asyncio.run(self.socketServer.startServer())


    def send_action(self, action):
        if self.socketServer:
            self.socketServer.sendAction(action)