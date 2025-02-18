from odyssey_kingdoms import MarioOdysseyKingdoms
from file_manager import ScreenshotManager
from actionHandling.socket_server import SocketServer
import asyncio
from stateParsing.state_parser import StateParser
import odyssey_state as State

class OdysseyWrapper:
    _fps = 60
    taking_screenshots = False
    game_cleared = False
    socketServer: SocketServer = None

    def __init__(self):
        self.start_action_server()
        self.reset()


    def reset(self):
        self.taking_screenshots = False
        State.regional_coins = { MarioOdysseyKingdoms.CAP: 0 }
        State.visited_kingdoms = set()
        State.coin_count = 0
        State.moon_count = 0
        self.game_cleared = False
        State.current_kingdom = MarioOdysseyKingdoms.CAP
        _ = input("Press enter when the Mario Odyssey game has started a new game file...")
        self.taking_screenshots = True
        asyncio.run(self.take_screenshots())
    

    async def take_screenshots(self):
        while self.taking_screenshots:
            await asyncio.sleep(1 / self.fps)
            ScreenshotManager.updateScreenshots()
            self.update_state()


    def recognize_text_handler(self, request, error):
        observations = request.results()
        results = []
        for observation in observations:
            # Return the string of the top VNRecognizedText instance.
            recognized_text = observation.topCandidates_(1)[0]
            results.append([recognized_text.string(), recognized_text.confidence()])
        
        multiMoonList = list(filter(lambda string: string.__contains__("YOU GOT A MULTI MOON!"), results))
        if multiMoonList:
            print("Received a multimoon!")
            State.moon_count += 3

        moonList = list(filter(lambda string: string.__contains__("GOT A MOON!"), results))
        if moonList:
            State.moon_count += 1

        kingdomNames = list(filter(lambda string: string.__contains__(" Kingdom"), results))
        if kingdomNames:
            kingdomName = kingdomNames[0]
            kingdom = MarioOdysseyKingdoms.CAP
            match kingdomName:
                case "Cap Kingdom": kingdom = MarioOdysseyKingdoms.CAP
                case "Cascade Kingdom": kingdom = MarioOdysseyKingdoms.CASCADE
                case "Sand Kingdom": kingdom = MarioOdysseyKingdoms.SAND
                case "Lake Kingdom": kingdom = MarioOdysseyKingdoms.LAKE
                case "Wooded Kingdom": kingdom = MarioOdysseyKingdoms.WOODED
                case "Cloud Kingdom": kingdom = MarioOdysseyKingdoms.CLOUD
                case "Lost Kingdom": kingdom = MarioOdysseyKingdoms.LOST
                case "Metro Kingdom": kingdom = MarioOdysseyKingdoms.METRO
                case "Snow Kingdom": kingdom = MarioOdysseyKingdoms.SNOW
                case "Seaside Kingdom": kingdom = MarioOdysseyKingdoms.SEASIDE
                case "Luncheon Kingdom": kingdom = MarioOdysseyKingdoms.LUNCHEON
                case "Ruined Kingdom": kingdom = MarioOdysseyKingdoms.RUINED
                case "Bowser's Kingdom": kingdom = MarioOdysseyKingdoms.BOWSERS
                case "Moon Kingdom": kingdom = MarioOdysseyKingdoms.MOON
            
            State.current_kingdom = kingdom
            State.visited_kingdoms.add(kingdom)


    def update_state(self):
        state = StateParser.getStateFrom(ScreenshotManager.current_screenshot_title, self.recognize_text_handler)
        coins = state[0]
        regionals = state[1]

        if coins > 0:
            State.coin_count = coins

        State.regional_coins[State.current_kingdom] = max(regionals, State.regional_coins[State.current_kingdom])

    def get_observations(self):
        return {
            "numCoins": State.coin_count,
            "regionalCoins": self.calculate_collected_regional_coins(),
            "moons": State.moon_count,
            "kingdoms": len(State.visited_kingdoms),
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
            "currentKingdom": State.current_kingdom,
            "regionalCoins": State.regional_coins
        }
    

    def calculate_collected_regional_coins(self):
        return sum(State.regional_coins.values())
    

    def start_action_server(self):
        self.socketServer = SocketServer()
        asyncio.run(self.socketServer.startServer())


    def send_action(self, action):
        if self.socketServer:
            self.socketServer.sendAction(action)

    
    