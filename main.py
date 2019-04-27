#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyglet
from game.grid import Grid
from game.utils import Position
from game.spell import MoveSpell, HarvestSpell
from game.enchantment import SimpleEnchantment
import game.resources as resources

window = pyglet.window.Window(visible=False)
window.set_caption('Legend Of Wizard')
window.set_visible()

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

grid = Grid()

enchantments = []
entities = []
minions = []
spells = [MoveSpell, HarvestSpell]

@window.event
def on_draw():
    window.clear()
    
    main_batch = pyglet.graphics.Batch()
    
    grid.draw(main_batch, Position(0, 0))
    
    main_batch.draw()

def update(dt):
    for entity in entities:
        entity.update(dt)

pyglet.clock.schedule_interval(update, 1/10)

if __name__ == '__main__':
    pyglet.app.run()
