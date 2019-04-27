class Entity:
    def __init__(self, sprite, enchantment, speed):
        self.sprite = sprite
        self.enchantment = enchantment
        self.speed = speed

        self.position = position

class SlimeEntity(Entity):
    def __init__(self, sprite, enchantment, speed, mind, item, life_spawn, special):
        super(sprite, enchantment, speed, mind, item, life_spawn, special)
        mind = 5
        item = 1
        life_spawn = 100
        special = None

class GoblinEntity(Entity):
    def __init__(self, sprite, enchantment, speed, mind, item, life_spawn, special):
        super(sprite, enchantment, speed, mind, item, life_spawn, special)
        mind = 7
        item = 5
        life_spawn = 100
        special = Launchable
