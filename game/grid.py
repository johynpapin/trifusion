import pyglet
from math import ceil
from .utils import Position
from . import resources

class Grid:
    def __init__(self):
        self.grid = {}
        self.camera = Position(0, 0)
        self.sprites = []

        self.get_tile(Position(0, 0)).resource = True

    def is_empty(self, position):
        return position not in self.grid

    def get_tile(self, position):
        if self.is_empty(position):
            self.grid[position] = Tile(position)

        return self.grid[position]

    def move_camera(self, dx, dy):
        self.camera.x -= dx
        self.camera.y -= dy

    def draw(self, batch, offset, size):
        start_x = self.camera.x // 70
        start_y = self.camera.y // 70

        camera_offset = Position(-self.camera.x % 70, self.camera.y % 70)

        for x in range(ceil((size[0] - offset.x + camera_offset.x) / 70.0)):
            for y in range(ceil((size[1] - offset.y + camera_offset.y) / 70.0)):
                tile = self.get_tile(Position(start_x + x, start_y + y))
                tile.draw(batch, Position(x * 70, size[1] - y * 70) + offset + camera_offset)


class Tile:
    def __init__(self, position):
        self.resource = None
        self.position = position

    def is_obstacle(self):
        return False

    def has_resource(self):
        return self.resource is not None

    def draw(self, batch, position):
        if self.has_resource():
            pass
        else:
            self.sprite = pyglet.sprite.Sprite(img=resources.grass_image, batch=batch)
            self.sprite.x = position.x
            self.sprite.y = position.y
