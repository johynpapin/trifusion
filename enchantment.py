class Enchantment:
    def __init__(self, name):
        self.name = name
        self.spells = []
        self.cost = 0

    def update_cost(self):
        self.cost = sum(spell.get_cost() for spell in self.spells)

    def insert_spell(self, index, *spells):
        for spell in spells:
            self.spells.insert(index, spell)
        
        self.update_cost()

class SimpleEnchantment(Enchantment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.insert_spell(MoveSpell(), HarvestSpell(), MoveSpell())
