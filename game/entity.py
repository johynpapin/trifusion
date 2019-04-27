import pyglet
from . import resources
from .enchantment import Executor
from .utils import Position

class Entity:
    def __init__(self, grid, enchantment, speed):
        self.grid = grid
        self.enchantment = enchantment
        self.speed = speed
        self.position = Position(0, 0)
        self.executor = Executor(self, enchantment)

    def update(self, dt):
        self.executor.update()

class SlimeEntity(Entity):
    def __init__(self, grid, enchantment):
        super().__init__(grid, enchantment, 30)

    def draw(self, batch, group, position):
        self.sprite = pyglet.sprite.Sprite(img=resources.slime_front_left_image, batch=batch, group=group)
        self.sprite.x = position.x
        self.sprite.y = position.y

class GoblinEntity(Entity):
    def __init__(self, sprite, enchantment, speed, mind, item, life_spawn, special):
        super(sprite, enchantment, speed, mind, item, life_spawn, special)
        mind = 7
        item = 5
        life_spawn = 100
        special = Launchable
