from .grid import Forest
from .utils import Position

class Spell:
    def __init__(self):
        self.cost = 1

class MoveSpell(Spell):
    def __init__(self, destination=Position(0, 0)):
        super().__init__()

        self.destination = destination

    def update(self, entity, state):
        if len(state) == 0:
            state['next_move'] = entity.speed
            state['resource_position'] = None

        if state['next_move'] != 0:
            state['next_move'] -= 1
            return (False,)

        path = None

        if isinstance(self.destination, Position):
            path = entity.grid.find_path(entity.position, self.destination)
        else:
            if state['resource_position'] is None or \
                not entity.grid.get_tile(state['resource_position']).has_resource() or \
                not isinstance(entity.grid.get_tile(state['resource_position']).resource, self.destination):
        
                state['resource_position'] = entity.grid.found_resource(entity.position, self.destination)

                if state['resource_position'] is None:
                    return (False,)
            
            path = entity.grid.find_path(entity.position, state['resource_position'])

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
            state['ticks_left'] = 30

        state['ticks_left'] -= 1

        if state['ticks_left'] > 0:
            return (False,)

        if isinstance(entity.grid.get_tile(entity.position).resource, Forest):
            entity.grid.get_tile(entity.position).resource = None
            entity.wood_count += 5

        return (True,)

class WaitSpell(Spell):
    def __init__(self):
        super().__init__()

    def update(self, entity, state):
        if len(state) == 0:
            pass

        return (False,)

class DropSpell(Spell):
    def __init__(self):
        super().__init__()

    def update(self, entity, state):
        entity.state.wood_count += entity.wood_count
        entity.wood_count = 0

        return (True,)
