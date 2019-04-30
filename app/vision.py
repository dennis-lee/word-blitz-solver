import cv2
import imutils
import numpy as np
import pytesseract

from tile import Tile

TARGET = (76, 21, 38)  # Color of the game window
BONUS_2W = (121, 56, 242)
BONUS_2L = (217, 200, 133)
BONUS_3L = (251, 144, 187)
lower = np.array([TARGET[0] - 10, TARGET[1] - 10, TARGET[2] - 38], dtype=np.uint8)
upper = np.array([TARGET[0] + 10, TARGET[1] + 10, TARGET[2] + 38], dtype=np.uint8)


class Vision:
    def __init__(self, image):
        self.screenshot = cv2.imread(image)
        self.screenshot_gray = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)
        self.screenshot_hsv = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2HSV)
        self.game_x = 0
        self.game_y = 0
        self.game_h = 0
        self.game_w = 0
        self.game_offset_h = 0

    def generate_tiles(self):
        game_window = self.crop_game()
        tiles = self.find_tiles(game_window)

        return self.arrange_tiles(tiles)

    def crop_game(self):
        print("Finding game window...")

        # Focus detection on game window
        window_mask = cv2.inRange(self.screenshot, lower, upper)
        game_window = cv2.bitwise_and(self.screenshot, self.screenshot, mask=window_mask)
        output_gray = cv2.cvtColor(game_window, cv2.COLOR_BGR2GRAY)
        output_blur = cv2.GaussianBlur(output_gray, (25, 25), 0)
        _, output_th = cv2.threshold(output_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Get window coordinates and dimension
        points = cv2.findNonZero(output_th)
        self.game_x, self.game_y, self.game_w, self.game_h = cv2.boundingRect(points)
        self.game_offset_h = int(self.game_h/3) - 32

        # Crop game window
        game_image = output_th[
                        self.game_y + self.game_offset_h:(self.game_y + self.game_h),
                        self.game_x:(self.game_x + self.game_w)
                     ].copy()
        game_image = cv2.bitwise_not(game_image)

        return game_image

    def find_tiles(self, game_window):
        print("Finding tiles...")

        # ref: https://docs.opencv.org/3.4/d3/db4/tutorial_py_watershed.html
        kernel = np.ones((25, 25), np.uint8)
        erosion = cv2.erode(game_window, kernel, iterations=2)
        dilate = cv2.dilate(erosion, kernel, iterations=2)

        # ref: https://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/
        contours = cv2.findContours(dilate.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        tiles = []

        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)

            if len(approx) == 4:
                x = approx[0][0][0]
                y = approx[0][0][1]
                tile_x = self.game_x + x
                tile_y = self.game_y + self.game_offset_h + y
                tile_width = int(peri/4)

                tile = self.screenshot_hsv[tile_y:tile_y + tile_width, tile_x:tile_x + tile_width].copy()
                tile_letter = self.extract_letter(tile)
                tile = Tile(letter=tile_letter,
                            x=tile_x + (tile_width/2),
                            y=tile_y + (tile_width/2)
                            )
                tiles.append(tile)

        return tiles

    @staticmethod
    def extract_letter(tile_image):
        lower_bg = np.array([0, 0, 0])
        upper_bg = np.array([330, 100, 93])
        mask = cv2.inRange(tile_image, lower_bg, upper_bg)

        tess_cfg = '-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ ' \
                   '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata" ' \
                   '--oem 0 ' \
                   '--psm 8'

        tess_cfg_default = '--oem 2 ' \
                        '--psm 10'

        result = pytesseract.image_to_string(mask, config=tess_cfg, lang='eng')

        print(result[0])

        return result[0]

    @staticmethod
    def arrange_tiles(tiles):
        sorted_y = sorted(tiles, key=lambda x: x.y)
        sorted_y = [sorted_y[i:i+4] for i in range(0, len(tiles), 4)]
        sorted_x = [sorted(row, key=lambda x: x.x) for row in sorted_y]

        return np.array(sorted_x)
