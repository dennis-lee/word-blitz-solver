from functools import reduce

LENGTH_BONUS = {
    2: 3,
    3: 4,
    4: 6,
    5: 7
    # TODO: add the remaining bonus values
}

class Word:
    def __init__(self, selected_tiles):
        self.tiles = selected_tiles
        self.score = 0

    def __len__(self):
        return len(self.tiles)

    def __repr__(self):
        return "".join([tile.letter for tile in self.tiles])

    def __eq__(self, other):
        return self.tiles == other.tiles

    def __hash__(self):
        return hash(tuple(self.tiles))

    def add_tile(self, tile):
        self.tiles.append(tile)

    def copy_tiles(self):
        return self.tiles.copy()

    def get_trail(self):
        return [(tile.x, tile.y) for tile in self.tiles]

    def total_score(self):
        sum_values = sum([tile.value for tile in self.tiles])
        bonus = 9 if len(self.tiles) > 8 else LENGTH_BONUS[len(self.tiles)]
        multiplier = reduce(lambda x, y: x * y, [tile.multiplier for tile in self.tiles])

        return (sum_values * multiplier) + bonus
