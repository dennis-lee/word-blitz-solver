import cv2
import imutils
import numpy as np

TARGET = (76, 21, 38)  # Color of the game window
BONUS_2W = (121, 56, 242)
BONUS_2L = (217, 200, 133)
BONUS_3L = (251, 144, 187)
lower = np.array([TARGET[0] - 10, TARGET[1] - 10, TARGET[2] - 38], dtype=np.uint8)
upper = np.array([TARGET[0] + 10, TARGET[1] + 10, TARGET[2] + 38], dtype=np.uint8)
TILE_LENGTH = 64

image = cv2.imread('resources/screenshot.png')

# Focus detection on game window
window_mask = cv2.inRange(image, lower, upper)
game_window = cv2.bitwise_and(image, image, mask=window_mask)
output_gray = cv2.cvtColor(game_window, cv2.COLOR_BGR2GRAY)
output_blur = cv2.GaussianBlur(output_gray, (25, 25), 0)
_, output_th = cv2.threshold(output_blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
points = cv2.findNonZero(output_th)
GAME_X, GAME_Y, GAME_W, GAME_H = cv2.boundingRect(points)
# cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

game_image = image[GAME_Y:GAME_Y + GAME_H, GAME_X:GAME_X + GAME_W].copy()
game_gray = cv2.cvtColor(game_image, cv2.COLOR_BGR2GRAY)
game_blur = cv2.GaussianBlur(game_gray, (45, 45), 0)
_, game_th = cv2.threshold(game_blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# ref: https://docs.opencv.org/3.4/d3/db4/tutorial_py_watershed.html
kernel = np.ones((3, 3), np.uint8)
erosion = cv2.erode(game_th, kernel, iterations=5)

# ref: https://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/
contours = cv2.findContours(erosion.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)

for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

    if len(approx) == 4:
        x = approx[0][0][0]
        y = approx[0][0][1]
        tile_x = GAME_X + x
        tile_y = GAME_Y + y
        cv2.rectangle(image, (tile_x, tile_y), (tile_x + 64, tile_y + 64), (0, 255, 0), 2)

cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
