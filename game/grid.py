import pyglet
from .utils import Position
from . import resources

class Grid:
    def __init__(self):
        self.grid = {}
        self.camera = Position(0, 0)
        self.sprites = []

    def is_empty(self, position):
        return position not in self.grid

    def get_tile(self, position):
        if self.is_empty(position):
            self.grid[position] = Tile(position)

        return self.grid[position]

    def draw(self, batch, offset):
        for x in range(10):
            for y in range (10):
                tile = self.get_tile(Position(x, y))
                tile.draw(batch, offset)

class Tile:
    def __init__(self, position):
        self.resource = None
        self.position = position

    def has_resource(self):
        return self.resource is not None

    def draw(self, batch, offset):
        self.sprite = pyglet.sprite.Sprite(img=resources.grass_image, batch=batch)
        self.sprite.x = self.position.x * 70 + offset.x
        self.sprite.y = self.position.y * 70 + offset.y
