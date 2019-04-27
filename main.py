#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyglet

window = pyglet.window.Window(visible=False)
window.set_caption('Legend Of Wizard')
window.set_visible()

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

level_label = pyglet.text.Label(text='Legend Of Wizard',
                                x=200, y=200, anchor_x='center')

enchantments = []
minions = []
spells = [move, arvest, wait]
@window.event
def on_draw():
    window.clear()

    level_label.draw()

if __name__ == '__main__':
    pyglet.app.run()
