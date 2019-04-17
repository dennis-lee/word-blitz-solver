from board import Board
from trie import Trie
from vision import Vision


if __name__ == '__main__':
    t = Trie('resources/words2.txt')

    i = 'start'
    while i != 'quit':
        b = input("New game? (Y/N)\n")  # Sample grid: 'aelb,cate,slir,ipas'

        if b == 'n' or b == 'N':
            break

        elif b == 'y' or b == 'Y':
            v = Vision('resources/screenshot.png')
            state = v.generate_tiles()

            b = Board(state, t.root)
            b.solve()
