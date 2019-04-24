class Tile:
    def __init__(self, letter, value, x, y):
        self.letter = str.lower(letter)
        self.value = int(value)
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
