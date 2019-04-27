from . import resources
from .enchantment import Executor 

class Entity:
    def __init__(self, sprite, enchantment, speed):
        self.sprite = sprite
        self.enchantment = enchantment
        self.speed = speed
        self.position = position
        self.executor = Executor(self, enchantment)

    def update(self):
        self.executor.update()

class SlimeEntity(Entity):
    def __init__(self, enchantment):
        sprite = pyglet.sprite.Sprite(img=resources.slime_front_left)
        super.__init__(sprite, enchantment, 30)

class GoblinEntity(Entity):
    def __init__(self, sprite, enchantment, speed, mind, item, life_spawn, special):
        super(sprite, enchantment, speed, mind, item, life_spawn, special)
        mind = 7
        item = 5
        life_spawn = 100
        special = Launchable
