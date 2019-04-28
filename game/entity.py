import pyglet
from . import resources
from .enchantment import Executor
from .utils import Position

class Entity:
    def __init__(self, grid, enchantment, state, speed, life):
        self.grid = grid
        self.enchantment = enchantment
        self.state = state
        self.speed = speed
        self.position = Position(0, 0)
        self.executor = Executor(self, enchantment)
        self.wood_count = 0
        self.ticks_left = life
        self.dead = False

    def update(self, dt):
        if self.dead:
            return

        self.executor.update()
        
        self.ticks_left -= 1
        if self.ticks_left == 0:
            self.dead = True

class SlimeEntity(Entity):
    def __init__(self, grid, enchantment, state):
        super().__init__(grid, enchantment, state, 5, 500)

    def draw(self, batch, group, position, scale):
        self.sprite = pyglet.sprite.Sprite(img=resources.images['slime_front_left'], batch=batch, group=group)
        self.sprite.x = position.x
        self.sprite.y = position.y
        self.sprite.scale = scale

class GoblinEntity(Entity):
    def __init__(self, sprite, enchantment, speed, mind, item, life_spawn, special):
        super(sprite, enchantment, speed, mind, item, life_spawn, special)
        mind = 7
        item = 5
        life_spawn = 100
        special = Launchable
