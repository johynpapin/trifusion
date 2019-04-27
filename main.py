#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyglet
from grid import Grid
from utils import Position

window = pyglet.window.Window(visible=False)
window.set_caption('Legend Of Wizard')
window.set_visible()

pyglet.resource.path = ['resources']
pyglet.resource.reindex()


grid = Grid()
entities = []

@window.event
def on_draw():
    window.clear()

    batch = grid.get_batch(Position(0, 0), grass_image)
    bach.draw()

def update(dt):
    for entity in entities:
        entity.update(dt)

pyglet.clock.schedule_interval(update, 1/10)

if __name__ == '__main__':
    pyglet.app.run()
