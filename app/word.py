class Word:
    def __init__(self, selected_tiles):
        self.tiles = selected_tiles

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
