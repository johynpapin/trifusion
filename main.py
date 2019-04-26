#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyglet

def create_window():
    window = pyglet.window.Window(visible=False)
    window.set_caption('Legend Of Wizard')
    window.set_visible()

window = create_window()

if __name__ == '__main__':
    pyglet.app.run()
