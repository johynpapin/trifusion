import pyglet
from math import ceil
from .utils import Position
from . import resources
    
def distance(A, B):
    return abs(A.x - B.x) + abs(A.y - B.y)

def lowest(end, Potential):
    tst = Potential[0]
    mini = [tst, distance(tst.Position, end)]

    for el in Potential:
        dst = distance(el.Position, end)
    
        if dst < mini[1]:
            mini = [el, dst]
    
    return mini[0]

def accessible_neighbour(point, end):
    l = []
    x = point.Position.x
    y = point.Position.y
    
    for el in [Position(x, y - 1), Position(x + 1, y), Position(x, y + 1), Position(x - 1, y)]:
        #if not is_obstacle(el):
        if True:
            l.append(Node(el, point, end))
    
    return l

def lowest_list(openlist):
    L = []
    LL = []
    for el in openlist:
        L.append(el.G + el.H)
    
    mini = min(L)
    
    i = 0
    for el in L:
        if el == mini:
            LL.append(openlist[i])
        i += 1
    
    L = []
    for el in LL:
        L.append(el.H)

    mini = min(L)
    
    i = 0
    for el in L:
        if el == mini:
            return LL[i]
        i += 1

class Node:
    def __init__(self,Position,Father,end):
        self.Position = Position
        self.Father = Father
        if Father == None:
            self.G = 0
        else :
            self.G = Father.G + 1
        self.H = distance(self.Position,end)

class Grid:
    def __init__(self):
        self.grid = {}
        self.camera = Position(0, 0)
        self.zoom = 1.0
        self.sprites = []

        # self.get_tile(Position(0, 0)).resource = True

    def is_empty(self, position):
        return position not in self.grid

    def get_tile(self, position):
        if self.is_empty(position):
            self.grid[position] = Tile(position)

        return self.grid[position]

    def move_camera(self, dx, dy):
        self.camera.x -= dx
        self.camera.y -= dy

    def draw(self, batch, background_group, entities_group, offset, size, entities):
        camera_offset = Position(-self.camera.x % 70, self.camera.y % 70)
        zoom = self.zoom

        start_x = self.camera.x // (70 * zoom)
        start_y = self.camera.y // (70 * zoom)
        
        size_x = ceil((size[0] - offset.x + camera_offset.x) / (70 * zoom))
        size_y = ceil((size[1] - offset.y + camera_offset.y) / (70 * zoom))

        for x in range(size_x):
            for y in range(size_y):
                tile = self.get_tile(Position(start_x + x, start_y + y))
                tile.draw(batch, background_group, Position(x * 70 * zoom, size[1] - y * 70 * zoom) + offset + camera_offset, zoom)

        for entity in entities:
            if entity.position.x >= start_x and entity.position.y >= start_y and \
                    entity.position.x - start_x < size_x and entity.position.y - start_y < size_y:
                entity.draw(batch, entities_group, Position((entity.position.x - start_x) * 70 * zoom, size[1] - (entity.position.y - start_y) * 70 * zoom) + offset + camera_offset, zoom)

    def find_path(self, start, end):
        if start == end:
            return []
        
        openlist = [Node(start, None, end)]
        forbiden = []
        
        while lowest_list(openlist).Position != end or openlist != []:
            current = lowest_list(openlist)
            oport = accessible_neighbour(current, end)
        
            for position_potential in oport:
                if position_potential.Position in forbiden:
                    oport.remove(position_potential)
            
            for position_seen in openlist:
                for potential_position in oport:
                    if potential_position.Position == position_seen.Position:
                        oport.remove(potential_position)
            
            if oport == []:
                forbiden.append(current.Position)
                openlist.remove(current)
                current = lowest_list(openlist)
            else:
                openlist.append(lowest(end, oport))
        
        if openlist == []:
            return None
        
        Path = [lowest_list(openlist)]
        
        while Path[-1].Father.Position != start:
            Path.append(Path[-1].Father)
        
        Pathfonded = []
        Path = Path.reverse()
        
        for el in Path:
            Pathfonded.append(el.Position)
        
        return Pathfonded

class Tile:
    def __init__(self, position):
        self.resource = None
        self.position = position

    def is_obstacle(self):
        return False

    def has_resource(self):
        return self.resource is not None

    def draw(self, batch, group, position, scale):
        if self.has_resource():
            pass
        else:
            self.sprite = pyglet.sprite.Sprite(img=resources.grass_image, batch=batch, group=group)
            self.sprite.x = position.x
            self.sprite.y = position.y
            self.sprite.scale = ceil(scale)