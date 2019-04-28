from .grid import Forest
from .utils import Position

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

        if state['next_move'] != 0:
            state['next_move'] -= 1
            return (False,)

        path = None

        if isinstance(self.destination, Position):
            path = entity.grid.find_path(entity.position, self.destination)
        else:
            resource_position = entity.grid.found_resource(entity.position, Forest)
            
            if resource_position is None:
                return (False,)

            path = entity.grid.find_path(entity.positoin, resource_position)

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

        self.cost = 1

    def update(self, entity, state):
        if len(state) == 0:
            pass

        if isinstance(entity.grid.get_tile().resource, Forest):
            entity.grid.get_tile().resource = None
            entity.state.wood_count += 5

        return (True,)

class WaitSpell(Spell):
    def __init__(self):
        super().__init__()

    def update(self, entity, state):
        if len(state) == 0:
            pass

        return (False,)

