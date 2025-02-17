import PIL
from PIL import ImageGrab
from PIL import Image
import numpy as np

class ScreenshotManager:
    previous_screenshot_title = "screenshots/previous_screenshot_"
    current_screenshot_title = "screenshots/current_screenshot.png"
    screenshot_file_type = ".png"


    def updateScreenshots():
        # Update Previous Screenshots
        for i in reversed(range(1, 8)):
            if i == 1:
                ScreenshotManager.move_file(
                    ScreenshotManager.current_screenshot_title,
                    ScreenshotManager.get_previous_image_name(i)
                )
            else:
                ScreenshotManager.move_file(
                    ScreenshotManager.get_previous_image_name(i - 1),
                    ScreenshotManager.get_previous_image_name(i)
                )

        # Take New Screenshot and Save to Current
        ScreenshotManager.take_screenshot(ScreenshotManager.current_screenshot_title)


    def move_file(source, destination):
        image = Image.open(source)
        image.save(destination)

    
    def take_screenshot(save_destination: str):
        screenshot = ImageGrab.grab()
        screenshot.save(save_destination, 'PNG')

    
    def get_image(source):
        image = Image.open(source)
        return np.array(image)
    

    def get_previous_image_name(number: int):
        return f'{ScreenshotManager.previous_screenshot_title}{number}{ScreenshotManager.screenshot_file_type}'