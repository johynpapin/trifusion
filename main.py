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

ui_state = {
    'tab_entities_focus': False,
    'tab_entities_hover': False,
    'tab_enchantments_focus': False,
    'tab_enchantments_hover': False,
    'tab_spells_focus': False,
    'tab_spells_hover': False,
    'tab_settings_focus': False,
    'tab_settings_hover': False
}

@window.event
def on_draw():
    window.clear()
    
    main_batch = pyglet.graphics.Batch()

    background_group = pyglet.graphics.OrderedGroup(0)
    resources_group = pyglet.graphics.OrderedGroup(1)
    entities_group = pyglet.graphics.OrderedGroup(2)
    ui_background_group = pyglet.graphics.OrderedGroup(3)
    ui_group = pyglet.graphics.OrderedGroup(4)
    
    ui_tabs_y = window.get_size()[1] - 30

    ui_header = pyglet.sprite.Sprite(resources.images['ui_header'], x=0, y=window.get_size()[1], batch=main_batch, group=ui_background_group)
    ui_footer = pyglet.sprite.Sprite(resources.images['ui_footer'], x=0, y=resources.images['ui_footer'].height, batch=main_batch, group=ui_background_group)

    if ui_state['tab_entities_focus']:
        ui_tab_entities = pyglet.sprite.Sprite(resources.images['ui_tab_entities_focus'], x=32, y=ui_tabs_y, batch=main_batch, group=ui_group)
    elif ui_state['tab_entities_hover']:
        ui_tab_entities = pyglet.sprite.Sprite(resources.images['ui_tab_entities_hover'], x=32, y=ui_tabs_y, batch=main_batch, group=ui_group)
    else:
        ui_tab_entities = pyglet.sprite.Sprite(resources.images['ui_tab_entities'], x=32, y=ui_tabs_y, batch=main_batch, group=ui_group)
    
    if ui_state['tab_enchantments_focus']:
        ui_tab_enchantments = pyglet.sprite.Sprite(resources.images['ui_tab_enchantments_focus'], x=141, y=ui_tabs_y, batch=main_batch, group=ui_group)
    elif ui_state['tab_enchantments_hover']:
        ui_tab_enchantments = pyglet.sprite.Sprite(resources.images['ui_tab_enchantments_hover'], x=141, y=ui_tabs_y, batch=main_batch, group=ui_group)
    else:
        ui_tab_enchantments = pyglet.sprite.Sprite(resources.images['ui_tab_enchantments'], x=141, y=ui_tabs_y, batch=main_batch, group=ui_group)
    
    if ui_state['tab_spells_focus']:
        ui_tab_spells = pyglet.sprite.Sprite(resources.images['ui_tab_spells_focus'], x=250, y=ui_tabs_y, batch=main_batch, group=ui_group)
    elif ui_state['tab_spells_hover']:
        ui_tab_spells = pyglet.sprite.Sprite(resources.images['ui_tab_spells_hover'], x=250, y=ui_tabs_y, batch=main_batch, group=ui_group)
    else:
        ui_tab_spells = pyglet.sprite.Sprite(resources.images['ui_tab_spells'], x=250, y=ui_tabs_y, batch=main_batch, group=ui_group)
    
    if ui_state['tab_settings_focus']:
        ui_tab_settings = pyglet.sprite.Sprite(resources.images['ui_tab_settings_focus'], x=359, y=ui_tabs_y, batch=main_batch, group=ui_group)
    elif ui_state['tab_settings_hover']:
        ui_tab_settings = pyglet.sprite.Sprite(resources.images['ui_tab_settings_hover'], x=359, y=ui_tabs_y, batch=main_batch, group=ui_group)
    else:
        ui_tab_settings = pyglet.sprite.Sprite(resources.images['ui_tab_settings'], x=359, y=ui_tabs_y, batch=main_batch, group=ui_group)

    ui_background_height = window.get_size()[1] - resources.images['ui_header'].height - resources.images['ui_footer'].height + 38

    ui_background = []
    for y in range(ui_background_height):
        ui_background.append(pyglet.sprite.Sprite(resources.images['ui_background'], x=0, y=resources.images['ui_footer'].height + y + 1, batch=main_batch, group=ui_background_group))

    grid.draw(main_batch, background_group, resources_group, entities_group, grid_offset, window.get_size(), entities)

    main_batch.draw()

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & pyglet.window.mouse.LEFT:
        if x >= grid_offset.x and y >= grid_offset.y:
            grid.move_camera(dx, -dy)

def is_position_in_rectangle(position, x, y, width, height):
    return x <= position.x and position.x <= x + width and y <= position.y and position.y <= y + height

@window.event
def on_mouse_motion(x, y, dx, dy):
    mouse_position = Position(x, window.get_size()[1] - y)

    ui_state['tab_entities_hover'] = is_position_in_rectangle(mouse_position, 32, 30, 106, 71)
    ui_state['tab_enchantments_hover'] = is_position_in_rectangle(mouse_position, 141, 30, 106, 71)
    ui_state['tab_spells_hover'] = is_position_in_rectangle(mouse_position, 250, 30, 106, 71)
    ui_state['tab_settings_hover'] = is_position_in_rectangle(mouse_position, 359, 30, 106, 71)

@window.event
def on_mouse_press(x, y, button, modifiers):
    mouse_position = Position(x, window.get_size()[1] - y)
    
    if button == pyglet.window.mouse.LEFT:
        ui_state['tab_entities_focus'] = is_position_in_rectangle(mouse_position, 32, 30, 106, 71)
        ui_state['tab_enchantments_focus'] = is_position_in_rectangle(mouse_position, 141, 30, 106, 71)
        ui_state['tab_spells_focus'] = is_position_in_rectangle(mouse_position, 250, 30, 106, 71)
        ui_state['tab_settings_focus'] = is_position_in_rectangle(mouse_position, 359, 30, 106, 71)

@window.event
def on_mouse_release(x, y, button, modifiers):
    mouse_position = Position(x, window.get_size()[1] - y)
    
    if button == pyglet.window.mouse.LEFT:
        ui_state['tab_entities_focus'] = False
        ui_state['tab_enchantments_focus'] = False
        ui_state['tab_spells_focus'] = False
        ui_state['tab_settings_focus'] = False

scroll = 0

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global scroll

    scroll += scroll_y

    grid.zoom = 1.1 ** scroll

def update(dt):
    for entity in entities:
        entity.update(dt)

pyglet.clock.schedule_interval(update, 1/10)

if __name__ == '__main__':
    pyglet.app.run()
