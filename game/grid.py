import pyglet
from math import ceil
from .utils import Position
from . import resources

class Node:
    def __init__(self,Position,Father,end):
        self.Position = Position
        self.Father = Father
        if Father = None:
            self.G = 0
        else :
            self.G = Father.G + 1
        self.H = distance(self.Position,end)

class Grid:
    def __init__(self):
        self.grid = {}
        self.camera = Position(0, 0)
        self.sprites = []

    def is_empty(self, position):
        return position not in self.grid

    def get_tile(self, position):
        if self.is_empty(position):
            self.grid[position] = Tile(position)

        return self.grid[position]

    def draw(self, batch, offset, size):
        for x in range(ceil((size[0] - offset.x) / 70.0)):
            for y in range(ceil((size[1] - offset.y) // 70.0)):
                tile = self.get_tile(Position(x, y))
                tile.draw(batch, offset, size)

    def distance(A,B):
        return(abs(A.x-B.x)+abs(A.y-B.y))

    def lowest(end,Potential):
        tst = Potential[0]
        mini = [dst,distance(tst, end)]
        for el in Potential:
            dst = distance(el.Position, end)
            if dst<mini[1]:
                mini = [el, dst]
        return mini[0]

    def accessible_neighbour(point,end):
        l = []
        x=point.Position.x
        y=point.Position.y
        for el in [Position(x, y-1), Position(x+1, y), Position(x, y+1), Position(x-1, y)]:
            if not(is_obstacle(el)):
                l.append(Node(el,point,end)
        return l

        def lowest_list(openlist):
            L = []
            LL = []
            for el in openlist:
                L.append(el.G+el.H)
            mini = min.L
            i = 0
            for el in L:
                if el == mini:
                    LL.append(openlist[i])
                i +=1
            L = []
            for el in LL:
                L.append(el.H)
            mini = min.L
            i = 0
            for el in L:
                if el == mini:
                    return(LL[i])
                i += 1

    def find_path(start,end):
        if start == end:
            return []
        openlist = [Node(start,None,end)]
        forbiden = []
        while Path[-1].Position != end or openlist != []:
            current = lowest_list(openlist)
            oport = accessible_neighbour(current)
            for position_potential in oport:
                if forbiden.content(position_potential.position):
                    oport.remove(position_potential)
            for position_seen in openlist:
                for potential_position in oport:
                    if potential_position.Position == position_seen.Position:
                        oport.remove(potentiel_position)
            if oport == []:
                forbiden.append(current.position)
                openlist.remove(current)
                current = lowest_list(openlist)
            else:
                openlist.append(lowest(end,oport))
        if openlist == []:
            return None
        Path = [lowest_list(openlist)]
        while Path[-1].Father.position != start:
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

    def draw(self, batch, offset, size):
        self.sprite = pyglet.sprite.Sprite(img=resources.grass_image, batch=batch)
        self.sprite.x = self.position.x * 70 + offset.x
        self.sprite.y = size[1] - self.position.y * 70 + offset.y
