from .spell import MoveSpell, HarvestSpell
from .utils import Position

class Enchantment:
    def __init__(self, name):
        self.name = name
        self.spells = []
        self.cost = 0

    def update_cost(self):
        self.cost = sum(spell.cost for spell in self.spells)

    def append_spell(self, *spells):
        for spell in spells:
            self.spells.append(spell)
        
        self.update_cost()

class SimpleEnchantment(Enchantment):
    def __init__(self, name):
        super().__init__(name)

        self.append_spell(MoveSpell(Position(10, 10)), HarvestSpell(), MoveSpell(Position(0, 0)))

class Executor():
    def __init__(self, entity, enchantment):
        self.entity = entity
        self.enchantment = enchantment
        self.current = None
        self.state = {}

    def update(self):
        if self.current is None:
            self.current = 0
            self.state = {}
        
        result = self.enchantment.spells[self.current].update(self.entity, self.state)

        if result[0] == True:
            if len(result) > 1:
                self.current = result[1]
            else:
                self.current += 1

            if self.current >= len(self.enchantment.spells):
                self.current = 0

            self.state = {} 
