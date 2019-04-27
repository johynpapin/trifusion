#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyglet
from game.grid import Grid
from game.entity import SlimeEntity
from game.utils import Position
from game.spell import MoveSpell, HarvestSpell
from game.enchantment import SimpleEnchantment
import game.resources as resources

window = pyglet.window.Window(visible=False, resizable=True)
window.set_caption('Legend Of Wizard')
window.set_visible()

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

grid_offset = Position(500, 0)
grid = Grid()

enchantments = []
entities = []
spells = [MoveSpell, HarvestSpell]

slime = SlimeEntity(grid, SimpleEnchantment("IA stupide"))
entities.append(slime)

@window.event
def on_draw():
    window.clear()
    
    main_batch = pyglet.graphics.Batch()
    background_group = pyglet.graphics.OrderedGroup(0)
    entities_group = pyglet.graphics.OrderedGroup(2)

    grid.draw(main_batch, background_group, entities_group, grid_offset, window.get_size(), entities)

    main_batch.draw()

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & pyglet.window.mouse.LEFT:
        if x >= grid_offset.x and y >= grid_offset.y:
            grid.move_camera(dx, -dy)

def update(dt):
    for entity in entities:
        entity.update(dt)

pyglet.clock.schedule_interval(update, 1/10)

if __name__ == '__main__':
    pyglet.app.run()
