import cv2
import imutils
import numpy as np
import pytesseract

TARGET = (76, 21, 38)  # Color of the game window
BONUS_2W = (121, 56, 242)
BONUS_2L = (217, 200, 133)
BONUS_3L = (251, 144, 187)
lower = np.array([TARGET[0] - 10, TARGET[1] - 10, TARGET[2] - 38], dtype=np.uint8)
upper = np.array([TARGET[0] + 10, TARGET[1] + 10, TARGET[2] + 38], dtype=np.uint8)
TILE_LENGTH = 64


class Vision:
    def __init__(self, image):
        self.screenshot = cv2.imread(image)
        self.screenshot_gray = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)
        self.game_x = 0
        self.game_y = 0
        self.game_h = 0
        self.game_w = 0

    def generate_tiles(self):
        game_window = self.crop_game()
        tiles = self.find_tiles(game_window)

        return tiles

    def crop_game(self):
        # Focus detection on game window
        window_mask = cv2.inRange(self.screenshot, lower, upper)
        game_window = cv2.bitwise_and(self.screenshot, self.screenshot, mask=window_mask)
        output_gray = cv2.cvtColor(game_window, cv2.COLOR_BGR2GRAY)
        output_blur = cv2.GaussianBlur(output_gray, (25, 25), 0)
        _, output_th = cv2.threshold(output_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Get window coordinates and dimension
        points = cv2.findNonZero(output_th)
        self.game_x, self.game_y, self.game_w, self.game_h = cv2.boundingRect(points)

        # Crop game window
        game_image = self.screenshot[
                        self.game_y:(self.game_y + self.game_h),
                        self.game_x:(self.game_x + self.game_w)
                     ].copy()
        game_gray = cv2.cvtColor(game_image, cv2.COLOR_BGR2GRAY)
        game_blur = cv2.GaussianBlur(game_gray, (45, 45), 0)
        _, game_th = cv2.threshold(game_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return game_th

    def find_tiles(self, game_window):
        # ref: https://docs.opencv.org/3.4/d3/db4/tutorial_py_watershed.html
        kernel = np.ones((3, 3), np.uint8)
        erosion = cv2.erode(game_window, kernel, iterations=5)

        # ref: https://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/
        contours = cv2.findContours(erosion.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        tiles = []

        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)

            if len(approx) == 4:
                x = approx[0][0][0]
                y = approx[0][0][1]
                tile_x = self.game_x + x
                tile_y = self.game_y + y
                # cv2.rectangle(image, (tile_x, tile_y), (tile_x + TILE_LENGTH, tile_y + TILE_LENGTH), (0, 255, 0), 1)
                tile = self.screenshot_gray[tile_y:tile_y + TILE_LENGTH, tile_x:tile_x + TILE_LENGTH].copy()
                tile = self.extract_letter(tile)
                tiles.append(tile)
                # break

        return tiles

    @staticmethod
    def extract_letter(tile_image):
        result = cv2.bitwise_not(tile_image)
        mask = cv2.inRange(result, np.array([205], dtype=np.uint8), np.array([255], dtype=np.uint8))
        target = cv2.bitwise_and(result, result, mask=mask)
        kernel = np.ones((2, 2), np.uint8)
        erode = cv2.erode(target, kernel, iterations=2)
        dilate = cv2.dilate(erode, kernel, iterations=3)
        result = cv2.bitwise_not(dilate)

        return pytesseract.image_to_string(result, config='--oem 1 --psm 10', lang='eng')
