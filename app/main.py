import pyautogui
import time

from board import Board
from trie import Trie
from vision import Vision


if __name__ == '__main__':
    pyautogui.PAUSE = 0.01
    pyautogui.FAILSAFE = True

    dictionary = 'resources/collins-scrabble.txt'
    t = Trie(dictionary)

    i = 'start'
    while i != 'quit':
        b = input("New game? (Y/N)\n")

        if b == 'n' or b == 'N':
            break

        elif b == 'y' or b == 'Y':
            # time.sleep(3)
            pyautogui.screenshot('screenshot.png')
            v = Vision('screenshot.png')
            state = v.generate_tiles()

            b = Board(state, t.root)
            b.solve()
