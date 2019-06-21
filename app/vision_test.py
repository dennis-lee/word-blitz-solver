import cv2
import imutils
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytesseract

def extract_letter_old(image):
    img = cv2.bitwise_not(image)
    # mask = cv2.inRange(img, np.array([190], dtype=np.uint8), np.array([255], dtype=np.uint8))
    # target = cv2.bitwise_and(img, img, mask=mask)
    # k = np.ones((2, 2), np.uint8)
    # e = cv2.erode(target, k, iterations=2)
    # d = cv2.dilate(target, k, iterations=1)
    # e = cv2.erode(d, k, iterations=2)
    # blur = cv2.GaussianBlur(d, (5, 5), 0)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # img = cv2.medianBlur(th, 1)
    tess_cfg = '-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ ' \
               '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata" ' \
               '--oem 0 ' \
               '--psm 7'

    tess_cfg_default = '--oem 2 ' \
                       '--psm 10'

    # letter_and_value = pytesseract.image_to_string(img, config=tess_cfg, lang='eng')
    # print(letter_and_value)
    # img = img[8:img.shape[0]-8, 8:img.shape[1]-8]

    return img

def extract_letter(image):
    lower_gray = np.array([0, 0, 0])
    upper_gray = np.array([330, 100, 93])
    upper_3L = np.array([132, 109, 255])
    mask = cv2.inRange(image, lower_gray, upper_gray)
    # mask = cv2.medianBlur(mask, 1)
    # res = cv2.bitwise_and(image, image, mask=mask)



    tess_cfg = '-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ ' \
               '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata" ' \
               '--oem 0 ' \
               '--psm 8'

    tess_cfg_default = '--oem 2 ' \
                       '--psm 10'

    letter_and_value = pytesseract.image_to_string(mask, config=tess_cfg, lang='eng')
    print(letter_and_value)

    return mask


TARGET = (76, 21, 38)  # Color of the game window
BONUS_2W = (121, 56, 242)
BONUS_2L = (217, 200, 133)
BONUS_3L = (251, 144, 187)
lower = np.array([TARGET[0] - 10, TARGET[1] - 10, TARGET[2] - 38], dtype=np.uint8)
upper = np.array([TARGET[0] + 10, TARGET[1] + 10, TARGET[2] + 38], dtype=np.uint8)

image = cv2.imread('screenshot.png')
image_gray = cv2.imread('screenshot.png', 0)
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Focus detection on game window
window_mask = cv2.inRange(image, lower, upper)
game_window = cv2.bitwise_and(image, image, mask=window_mask)
output_gray = cv2.cvtColor(game_window, cv2.COLOR_BGR2GRAY)
output_hsv = cv2.cvtColor(game_window, cv2.COLOR_BGR2HSV)
output_blur = cv2.GaussianBlur(output_gray, (25, 25), 0)
_, output_th = cv2.threshold(output_blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
points = cv2.findNonZero(output_th)
GAME_X, GAME_Y, GAME_W, GAME_H = cv2.boundingRect(points)
# cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# game_image = image[GAME_Y:GAME_Y + GAME_H, GAME_X:GAME_X + GAME_W].copy()
# game_gray = cv2.cvtColor(game_image, cv2.COLOR_BGR2GRAY)
# game_blur = cv2.GaussianBlur(game_gray, (25, 25), 0)
# _, game_th = cv2.threshold(game_blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

game_image = output_th[GAME_Y:GAME_Y + GAME_H, GAME_X:GAME_X + GAME_W].copy()
game_image = cv2.bitwise_not(game_image)

# ref: https://docs.opencv.org/3.4/d3/db4/tutorial_py_watershed.html
kernel = np.ones((20, 20), np.uint8)
erosion = cv2.erode(game_image, kernel, iterations=2)
dilate = cv2.dilate(erosion, kernel, iterations=2)
# erosion = cv2.erode(dilate, kernel, iterations=5)

# ref: https://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/
contours = cv2.findContours(dilate.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)

test = None
tiles = []

for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

    if len(approx) == 4:
        x = approx[0][0][0]
        y = approx[0][0][1]
        tile_x = GAME_X + x - 4
        tile_y = GAME_Y + y - 4
        tile_width = int(peri / 4) + 4

        # cv2.rectangle(image, (tile_x, tile_y), (tile_x + tile_width, tile_y + tile_width), (0, 255, 0), 1)
        tile = image_hsv[tile_y:tile_y+tile_width, tile_x:tile_x+tile_width].copy()
        tile = extract_letter(tile)
        tiles.append(tile)
        # break

cv2.imshow('image', image_hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Display and/or save images
titles = None
n_images = len(tiles)
if titles is None:
    titles = ['Image (%d)' % i for i in range(1, n_images + 1)]
fig = plt.figure()
for n, (image, title) in enumerate(zip(tiles, titles)):
    a = fig.add_subplot(4, np.ceil(n_images/float(4)), n + 1)
    if image.ndim == 2:
        plt.gray()
    plt.imshow(image, cmap='hsv')
    a.set_title(title)
    # plt.imsave("sample_tiles/{}.png".format(str(np.random.randint(1000))), image)
fig.set_size_inches(np.array(fig.get_size_inches()) * n_images)
plt.show()
