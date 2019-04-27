from utils import Position
import pyglet

class Grid:
    def __init__(self):
        self.grid = {}
        self.camera = Position(0, 0)

    def is_empty(self, position):
        return position not in self.grid

    def get_tile(self, position):
        if self.is_empty(position):
            self.grid[position] = Tile()

        return self.grid[position]

    def get_batch(self, offset, grass_image):
        batch = Batch()
        
        for x in range(10):
            for y in range (10):
                if self.is_empty(Position(x, y)):
                    sprite = pyglet.sprite.Sprite(grass_image)
                    sprite.x = offset.x + x * 70
                    sprite.y = offset.y + y * 70
                    batch.add(sprite)

        return batch

class Tile:
    def __init__():
        self.resource = None

    def has_resource(self):
        return self.resource is not None
