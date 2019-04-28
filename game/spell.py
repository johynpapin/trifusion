from .grid import Road
class Spell:
    def __init__(self):
        self.cost = 1

class MoveSpell(Spell):
    def __init__(self, destination):
        super().__init__()

        self.destination = destination

    def update(self, entity, state):
        if len(state) == 0:
            state['next_move'] = entity.speed
            position = entity.position
            if isinstance(entity.grid.grid[position].resource, Road):
                state['next_move'] = entity.speed*2

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

        state['next_move'] = entity.speed

        return (False,)

class HarvestSpell(Spell):
    def __init__(self):
        super().__init__()

    def update(self, entity, state):
        if len(state) == 0:
            pass
        
        return (True,)

class WaitSpell(Spell):
    def __init__(self):
        super().__init__()

    def update(self, entity, state):
        if len(state) == 0:
            pass

        return (False,)
