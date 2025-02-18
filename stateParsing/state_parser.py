from PIL import Image
import numpy as np
import Quartz
from Foundation import NSURL, NSRange
import Vision
import pytesseract

class StateParser:
    def trim_leading_zeros(num_str):
        """Removes leading zeros from a string.

        Args:
        num_str: The string to trim.

        Returns:
        The trimmed string, or "0" if the input string consists only of zeros.
        """
        for i, char in enumerate(num_str):
            if char != '0':
                return num_str[i:]
        return "0"

    def clean_ocr_detected_numbers(num_str):
        output = ""
        for char in num_str:
            if char == 'l' or char == '!':
                output += '1'
                continue
            if char == 'H':
                output += '4'
                continue
            if char == 'Z' or char == 'z':
                output += '2'
                continue
            if char == 'S' or char == 's':
                output += '5'
                continue
            if char == 'G':
                output += '6'
                continue
            if char == 'o' or char == 'O':
                output += '0'
                continue
        
            if ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'].__contains__(char):
                output += char
                continue

        return output

    def getStateFrom(screenshot, appleVisionCallback):
        # Get the CIImage on which to perform requests.
        input_url = NSURL.fileURLWithPath_(screenshot)
        input_image = Quartz.CIImage.imageWithContentsOfURL_(input_url)

        # Create a new image-request handler.
        request_handler = Vision.VNImageRequestHandler.alloc().initWithCIImage_options_(
                input_image, None
        )

        # Create a new request to recognize text.
        request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(appleVisionCallback)

        # Perform the text-recognition request.
        error = request_handler.performRequests_error_([request], None)

        pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
        img = Image.open(screenshot) 
        coinCropBox = (452, 69, 573, 123) 
        coinImg = img.crop(coinCropBox)
        coinImg = coinImg.convert("L")
        coinCount = pytesseract.image_to_string(coinImg, config='--psm 13') 
        coinCount = int(StateParser.trim_leading_zeros(StateParser.clean_ocr_detected_numbers(coinCount)))

        regionalsCropBox = (640, 57, 735, 114)
        regionalsImage = img.crop(regionalsCropBox).convert("L")
        regionalsCount = pytesseract.image_to_string(regionalsImage, config='--psm 13')
        regionalsCount = int(StateParser.trim_leading_zeros(StateParser.clean_ocr_detected_numbers(regionalsCount)))

        return [coinCount if coinCount > 0 else -1, regionalsCount]

        



def recognize_text_handler(request, error):
        observations = request.results()
        results = []
        for observation in observations:
            # Return the string of the top VNRecognizedText instance.
            recognized_text = observation.topCandidates_(1)[0]
            results.append(recognized_text.string())

        print(results)
        
        multiMoonList = list(filter(lambda string: string.__contains__("YOU GOT A MULTI MOON!"), results))
        if multiMoonList:
            print("Received a multimoon!")

        moonList = list(filter(lambda string: string.__contains__("GOT A MOON!"), results))
        if moonList:
            print("Received a moon!")

        kingdomNames = list(filter(lambda string: string.__contains__(" Kingdom"), results))
        if kingdomNames:
            print(f"In {kingdomNames[0]}")

state = StateParser.getStateFrom("stateParsing/testScreenshots/Screenshot 2025-02-18 083541.png", recognize_text_handler)
print(state)