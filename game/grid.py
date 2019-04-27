import pyglet
from math import ceil
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

    def draw(self, batch, offset, size):
        for x in range(ceil((size[0] - offset.x) / 70.0)):
            for y in range(ceil((size[1] - offset.y) // 70.0)):
                tile = self.get_tile(Position(x, y))
                tile.draw(batch, offset, size)

    def find_path(start,end):
        
class Tile:
    def __init__(self, position):
        self.resource = None
        self.position = position

    def has_resource(self):
        return self.resource is not None

    def draw(self, batch, offset, size):
        self.sprite = pyglet.sprite.Sprite(img=resources.grass_image, batch=batch)
        self.sprite.x = self.position.x * 70 + offset.x
        self.sprite.y = size[1] - self.position.y * 70 + offset.y
