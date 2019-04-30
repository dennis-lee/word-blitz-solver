TILE_VALUE = {
    'a': 1,
    'b': 3,
    'c': 3,
    'd': 2,
    'e': 1,
    'f': 4,
    'g': 2,
    'h': 4,
    'i': 1,
    'j': 8,
    'k': 5,
    'l': 1,
    'm': 3,
    'n': 1,
    'o': 1,
    'p': 3,
    'q': 10,
    'r': 1,
    's': 1,
    't': 1,
    'u': 1,
    'v': 4,
    'w': 4,
    'x': 8,
    'y': 4,
    'z': 10
}

class Tile:
    def __init__(self, letter, x, y):
        self.letter = str.lower(letter)
        self.value = TILE_VALUE[self.letter]
        self.x = x
        self.y = y
        self.nw = None
        self.n = None
        self.ne = None
        self.w = None
        self.e = None
        self.sw = None
        self.s = None
        self.se = None

    def __repr__(self):
        return self.letter

    def get_neighbours(self):
        neighbours = {self.nw, self.n, self.ne, self.w, self.e, self.sw, self.s, self.se}
        neighbours.discard(None)

        return neighbours
