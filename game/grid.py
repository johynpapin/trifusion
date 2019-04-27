import pyglet
from . import utils
from . import resources

class Grid:
    def __init__(self):
        self.grid = {}
        self.camera = utils.Position(0, 0)

    def is_empty(self, position):
        return position not in self.grid

    def get_tile(self, position):
        if self.is_empty(position):
            self.grid[position] = Tile()

        return self.grid[position]

    def get_batch(self, offset):
        batch = pyglet.graphics.Batch()
        
        for x in range(10):
            for y in range (10):
                if self.is_empty(utils.Position(x, y)):
                    sprite = pyglet.sprite.Sprite(img=resources.grass_image, batch=batch, x=offset.x + x * 70, y=offset.y + y * 70)

        return batch

class Tile:
    def __init__():
        self.resource = None

    def has_resource(self):
        return self.resource is not None
