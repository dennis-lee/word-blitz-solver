import numpy as np


class Board:
    def __init__(self, state, trie):
        self.trie = trie
        self.tiles = []

        self.map_tiles(state)

    def map_tiles(self, state):
        print("Mapping tiles...")

        board = np.pad(state, (1, 1), 'constant', constant_values='0')
        padded_board = np.empty((board.shape[0], board.shape[1]), dtype=object)

        for y in range(1, board.shape[0] - 1):
            for x in range(1, board.shape[1] - 1):
                padded_board[y, x] = board[y, x]

        for y in range(1, padded_board.shape[0] - 1):
            for x in range(1, padded_board.shape[1] - 1):
                t = padded_board[y, x]
                t.nw, t.n, t.ne = padded_board[y - 1, x - 1], padded_board[y - 1, x], padded_board[y - 1, x + 1]
                t.w, t.e = padded_board[y, x - 1], padded_board[y, x + 1]
                t.sw, t.s, t.se = padded_board[y + 1, x - 1], padded_board[y + 1, x], padded_board[y + 1, x + 1]

                self.tiles.append(t)

    def solve(self):
        print("Solving...")

        def __build_words(current_tile, current_node, selected_tiles, current_word, valid_words):
            if not len(current_node.children):
                valid_words.add(current_word)

            else:
                if current_node.acceptable:
                    valid_words.add(current_word)

                selected_tiles.add(current_tile)

                neighbours = current_tile.get_neighbours() - selected_tiles

                for neighbour in neighbours:
                    if neighbour.letter in current_node.children:
                        next_node = current_node.get_child(neighbour.letter)
                        new_word = '{}{}'.format(current_word, neighbour.letter)

                        __build_words(
                            neighbour,
                            next_node,
                            selected_tiles.copy(),
                            new_word,
                            valid_words
                        )

        total_words = 0

        for tile in self.tiles:
            words = set()
            __build_words(
                tile,
                self.trie.get_child(tile.letter),
                set(),
                tile.letter,
                words
            )

            total_words += len(words)

            if len(words):
                print('### {}'.format(tile))
                print(sorted(list(words), key=len, reverse=True))

        print("\nTotal words: {}\n".format(total_words))
