class Spell:
    def __init__(self):
        pass

    def get_cost(self):
        return self.cost

class MoveSpell(Spell):
    def __init__(self, destination):
        super()

        self.destination = destination

    def update(self, entity, state):
        if len(state) == 0:
            state['next_move'] = entity.speed

        if state['next_move'] != 0:
            state['next_move'] -= 1
            return (False,)

        path = entity.grid.find_path(entity.position, self.destination)
        
        if path is None:
            return (False,)

        if len(path) == 0:
            return (True,)

        entity.position = path[0]

        if len(path) == 1:
            return (True,)

class HarvestSpell(Spell):
    def __init__(self):
        super()

    def update(self, entity, state):
        if len(state) == 0:
            pass

class WaitSpell(Spell):
    def __init__(self):
        super()

    def update(self, entity, state):
        if len(state) == 0:
            pass
