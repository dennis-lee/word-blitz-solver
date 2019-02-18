from board import Board
from trie import Trie


if __name__ == '__main__':
    t = Trie('resources/words2.txt')

    i = 'start'
    while i != 'quit':
        b = input("Enter grid:\n")  # Sample grid: 'aelb,cate,slir,ipas'

        if b == 'quit':
            break

        b = Board(b, t.root)
        b.solve()
