#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyglet
from game.grid import Grid
from game.entity import SlimeEntity, GoblinEntity, OrcEntity
from game.utils import Position
from game.spell import MoveSpell, HarvestSpell, DropSpell
from game.enchantment import SimpleEnchantment
import game.resources as resources

window = pyglet.window.Window(visible=False, resizable=True)
window.set_caption('Legend Of Wizard')
window.set_visible()

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

pyglet.resource.add_font('04b_30.ttf')
pyglet.resource.add_font('04b_03.ttf')

grid_offset = Position(500, 0)
grid = Grid()

e0 = SimpleEnchantment("IA stupide")

enchantments = [e0]
entities = []
spells = [MoveSpell, HarvestSpell, DropSpell]

class GameState:
    def __init__(self):
        self.enchantment_boxes = []
        self.spell_boxes = []
        self.wood_count = 0

state = GameState()

for _ in range(5):
    slime = SlimeEntity(grid, e0, state)
    entities.append(slime)

def on_click_buy_slime():
    if state.wood_count >= 20:
        state.wood_count -= 20
        entities.append(SlimeEntity(grid, e0, state))

def on_click_buy_goblin():
    if state.wood_count >= 50:
        state.wood_count -= 50
        entities.append(GoblinEntity(grid, e0, state))

def on_click_buy_orc():
    if state.wood_count >= 20:
        state.wood_count -= 20
        entities.append(OrcEntity(grid, e0, state))

buttons = set()

class Button():
    def __init__(self, image, hover_image, focus_image, on_click, draggable=False):
        global buttons

        self.hover = False
        self.focus = False

        self.image = resources.images[image]
        self.hover_image = resources.images[hover_image]
        self.focus_image = resources.images[focus_image]

        self.draggable = draggable

        self.on_click = on_click

        buttons.add(self)

        self.last_position = Position(0, 0)

    def draw(self, batch, group, position, top_group=None):
        self.last_position = Position(position.x, window.get_size()[1] - position.y)

        if self.focus:
            self.sprite = pyglet.sprite.Sprite(self.focus_image, x=position.x, y=position.y, batch=batch, group=group)
        elif self.hover:
            self.sprite = pyglet.sprite.Sprite(self.hover_image, x=position.x, y=position.y, batch=batch, group=group)
        else:
            self.sprite = pyglet.sprite.Sprite(self.image, x=position.x, y=position.y, batch=batch, group=group)

class MoveSpellButton(Button):
    def __init__(self, spell):
        super().__init__('ui_spell_box_move', 'ui_spell_box_move', 'ui_spell_box_move', self.on_click, True)
        self.mode = True
        self.spell = spell

    def set_resource_mode(self, mode):
        self.mode = mode

        if mode:
            self.image = resources.images['ui_spell_box_move_resource']
        else:
            self.image = resources.images['ui_spell_box_move']

        self.hover_image = self.image
        self.focus_image = self.image

    def draw(self, batch, group, position, top_group):
        super().draw(batch, group, position)

        if self.mode:
            self.wood_sprite = pyglet.sprite.Sprite(resources.images['bois'], x=self.last_position.x + 200, y=window.get_size()[1] - self.last_position.y - 70, group=top_group, batch=batch)
        else:
            self.x_label = pyglet.text.Label(str(self.spell.destination.x), font_name='04b_03b', font_size=20, x=self.last_position.x + 183, y=window.get_size()[1] - self.last_position.y - 21, batch=batch, group=top_group, anchor_y='top', anchor_x='left')
            self.y_label = pyglet.text.Label(str(self.spell.destination.y), font_name='04b_03b', font_size=20, x=self.last_position.x + 183, y=window.get_size()[1] - self.last_position.y - 53, batch=batch, group=top_group, anchor_y='top', anchor_x='left')

    def on_click(self):
        if not self.mode:
            ui_state['waiting_for_position'] = self.spell

ui_state = {
    'tab_entities_focus': False,
    'tab_entities_hover': False,
    'tab_enchantments_focus': False,
    'tab_enchantments_hover': False,
    'tab_spells_focus': False,
    'tab_spells_hover': False,
    'tab_settings_focus': False,
    'tab_settings_hover': False,

    'return_button': None,

    'add_button': None,

    'quit_button': None,

    'window': False,
    'game_over': False,

    'buy_button_slime': Button('acheter_slime', 'acheter_slime_hover', 'acheter_slime_focus', on_click_buy_slime),

    'buy_button_goblin': Button('acheter_goblin', 'acheter_goblin_hover', 'acheter_goblin_focus', on_click_buy_goblin),

    'buy_button_orc': Button('acheter_orc', 'acheter_orc_hover', 'acheter_orc_focus', on_click_buy_orc),

    'current_tab': 0,
    'current_enchantment': None,
    'spells_order': [],

    'spell_buttons': [],

    'waiting_for_position': None
}

@window.event
def on_draw():
    global spell_boxes

    not_edible = []

    window.clear()

    main_batch = pyglet.graphics.Batch()

    background_group = pyglet.graphics.OrderedGroup(0)
    resources_group = pyglet.graphics.OrderedGroup(1)
    entities_group = pyglet.graphics.OrderedGroup(2)
    ui_background_group = pyglet.graphics.OrderedGroup(3)
    ui_group = pyglet.graphics.OrderedGroup(4)
    ui_top_group = pyglet.graphics.OrderedGroup(5)
    ui_new_window_group = pyglet.graphics.OrderedGroup(6)
    ui_on_window_group = pyglet.graphics.OrderedGroup(7)
    ui_on_on_window_group = pyglet.graphics.OrderedGroup(8)

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

    header_height = 125

    if ui_state['current_tab'] == 1:
        if ui_state['current_enchantment'] is None:
            for i, (enchantment, button) in enumerate(zip(enchantments, state.enchantment_boxes)):
                position = Position(50, window.get_size()[1] - (header_height + i * (resources.images['ui_enchantment_box'].height + 5)))
                button.draw(main_batch, ui_group, position)
                not_edible.append(pyglet.text.Label(enchantment.name, font_name='04b_03b', font_size=18, x=position.x + 70, y=position.y - 20, batch=main_batch, group=ui_top_group, anchor_x='left', anchor_y='top'))
        else:
            enchantment = enchantments[ui_state['current_enchantment']]

            ui_state['return_button'].draw(main_batch, ui_top_group, Position(35, window.get_size()[1] - header_height + 17))

            ui_state['add_button'].draw(main_batch, ui_top_group, Position(395, 75))

            if ui_state['window'] :
                modal_x = window.get_size()[0] // 2 - resources.images['fenetre'].width // 2
                modal_y = window.get_size()[1] // 2 - resources.images['fenetre'].height // 2
                not_edible.append(pyglet.sprite.Sprite(resources.images['fenetre'], x=modal_x, y=window.get_size()[1] - modal_y, batch=main_batch, group=ui_new_window_group))
                ui_state['quit_button'].draw(main_batch, ui_on_window_group, Position(modal_x + 550, window.get_size()[1] - modal_y - 30))

                for i, button in enumerate(ui_state['spell_buttons']):
                    button.draw(main_batch, ui_on_window_group, Position(modal_x + 100, window.get_size()[1] - modal_y - 30 - (button.image.height + 5) * i))
                    position = Position(modal_x + 100, window.get_size()[1] - modal_y - 30 - (button.image.height + 5) * i)
                    not_edible.append(pyglet.sprite.Sprite(resources.images['spell_' + spells[i].__name__[:-5].lower()], x=position.x + 30, y=position.y - 25, batch=main_batch, group=ui_on_on_window_group))

            not_edible.append(pyglet.sprite.Sprite(resources.images['ui_enchantment_cost'], x=402, y=window.get_size()[1] - header_height + 22, batch=main_batch, group=ui_group))
            not_edible.append(pyglet.text.Label(str(enchantment.cost), font_name='04b_03b', font_size=20, x=418, y=window.get_size()[1] - header_height + 15, batch=main_batch, group=ui_top_group, anchor_y='top', anchor_x='left'))

            for j, i in enumerate(ui_state['spells_order']):
                spell = enchantment.spells[i]
                button = state.spell_boxes[i]
                position = Position(50, window.get_size()[1] - (header_height + 30 + j * (resources.images['ui_spell_box'].height + 5)))
                button.draw(main_batch, ui_group, position, ui_top_group)
                not_edible.append(pyglet.text.Label(str(spell.cost), font_name='04b_03b', font_size=20, x=position.x + 275, y=position.y - 37, batch=main_batch, group=ui_top_group))
                not_edible.append(pyglet.sprite.Sprite(resources.images['spell_' + type(spell).__name__[:-5].lower()], x=position.x + 30, y=position.y - 25, batch=main_batch, group=ui_top_group))

    if ui_state['current_tab'] == 0:
        not_edible.append(pyglet.sprite.Sprite(resources.images['boite_a_bois'], x=50, y=window.get_size()[1] - 120, batch=main_batch, group=ui_group))
        not_edible.append(pyglet.text.Label(str(state.wood_count), font_name='04b_03b', font_size=12, x=95, y=window.get_size()[1] - 180, batch=main_batch, group=ui_top_group, anchor_x='left', anchor_y='top'))

        not_edible.append(pyglet.sprite.Sprite(resources.images['boite_a_slime'], x=150, y=window.get_size()[1] - 120, batch=main_batch, group=ui_group))
        not_edible.append(pyglet.text.Label(str(len(list(filter(lambda e: isinstance(e, SlimeEntity), entities)))), font_name='04b_03b', font_size=12, x=195, y=window.get_size()[1] - 180, batch=main_batch, group=ui_top_group, anchor_x='left', anchor_y='top'))

        not_edible.append(pyglet.sprite.Sprite(resources.images['boite_a_goblin'], x=250, y=window.get_size()[1] - 120, batch=main_batch, group=ui_group))
        not_edible.append(pyglet.text.Label(str(len(list(filter(lambda e: isinstance(e, GoblinEntity), entities)))), font_name='04b_03b', font_size=12, x=295, y=window.get_size()[1] - 180, batch=main_batch, group=ui_top_group, anchor_x='left', anchor_y='top'))

        not_edible.append(pyglet.sprite.Sprite(resources.images['boite_a_orc'], x=350, y=window.get_size()[1] - 120, batch=main_batch, group=ui_group))
        not_edible.append(pyglet.text.Label(str(len(list(filter(lambda e: isinstance(e, OrcEntity), entities)))), font_name='04b_03b', font_size=12, x=395, y=window.get_size()[1] - 180, batch=main_batch, group=ui_top_group, anchor_x='left', anchor_y='top'))


        ui_state['buy_button_slime'].draw(main_batch, ui_top_group, Position(35, window.get_size()[1] -  230))

        ui_state['buy_button_goblin'].draw(main_batch, ui_top_group, Position(190, window.get_size()[1] -  230))

        ui_state['buy_button_orc'].draw(main_batch, ui_top_group, Position(35, window.get_size()[1] -  390))

    if ui_state['game_over']:
        not_edible.append(pyglet.text.Label('Game over', font_name='04b_03b', font_size=60, x=window.get_size()[0] // 2, y=window.get_size()[1] // 2, anchor_x='center', anchor_y='center', group=ui_on_window, batch=main_batch))

    grid.draw(main_batch, background_group, resources_group, entities_group, grid_offset, window.get_size(), entities)

    main_batch.draw()

@window.event
def on_mouse_drag(x, y, dx, dy, ebuttons, modifiers):
    if ebuttons & pyglet.window.mouse.LEFT:
        if x >= grid_offset.x and y >= grid_offset.y:
            grid.move_camera(dx, -dy)
        else:
            for button in buttons.copy():
                if button.draggable and button.focus:
                    button.on_drag(button, x, y, dx, dy)

def is_position_in_rectangle(position, x, y, width, height):
    return x <= position.x and position.x <= x + width and y <= position.y and position.y <= y + height



@window.event
def on_mouse_motion(x, y, dx, dy):
    mouse_position = Position(x, window.get_size()[1] - y)

    ui_state['tab_entities_hover'] = is_position_in_rectangle(mouse_position, 32, 30, 106, 71)
    ui_state['tab_enchantments_hover'] = is_position_in_rectangle(mouse_position, 141, 30, 106, 71)
    ui_state['tab_spells_hover'] = is_position_in_rectangle(mouse_position, 250, 30, 106, 71)
    ui_state['tab_settings_hover'] = is_position_in_rectangle(mouse_position, 359, 30, 106, 71)

    for button in buttons.copy():
        button.hover = is_position_in_rectangle(mouse_position, button.last_position.x, button.last_position.y, button.image.width, button.image.height)

@window.event
def on_mouse_press(x, y, button, modifiers):
    mouse_position = Position(x, window.get_size()[1] - y)

    if button == pyglet.window.mouse.LEFT:
        if x >= grid_offset.x and y >= grid_offset.y and ui_state['waiting_for_position'] is not None:
            ui_state['waiting_for_position'].destination = grid.get_position(grid_offset, window.get_size(), x, y)
            ui_state['waiting_for_position'] = None

        ui_state['tab_entities_focus'] = is_position_in_rectangle(mouse_position, 32, 30, 106, 71)
        ui_state['tab_enchantments_focus'] = is_position_in_rectangle(mouse_position, 141, 30, 106, 71)
        ui_state['tab_spells_focus'] = is_position_in_rectangle(mouse_position, 250, 30, 106, 71)
        ui_state['tab_settings_focus'] = is_position_in_rectangle(mouse_position, 359, 30, 106, 71)

        for button in buttons.copy():
            button.focus = is_position_in_rectangle(mouse_position, button.last_position.x, button.last_position.y, button.image.width, button.image.height)

def generate_enchantments():
    buttons.clear()
    state.enchantment_boxes = []

    for i, enchantment in enumerate(enchantments):
        def generate_on_click(i):
            def on_click():
                buttons.clear()

                def generate_on_click_but_for_spell(i):
                    def on_click():
                        pass

                    return on_click

                def generate_on_drag_still_for_spell(spell_index, enchantment_index):
                    def on_drag(current_spell_box, x, y, dx, dy):
                        for j, spell_box in enumerate(state.spell_boxes):
                            mouse_position = Position(x, window.get_size()[1] - y)

                            if spell_box.index != current_spell_box.index and \
                                is_position_in_rectangle(mouse_position, spell_box.last_position.x, spell_box.last_position.y, spell_box.image.width, spell_box.image.height):
                                ui_state['spells_order'][current_spell_box.index], ui_state['spells_order'][spell_box.index] = ui_state['spells_order'][spell_box.index], ui_state['spells_order'][current_spell_box.index]
                                spell_box.index, current_spell_box.index = current_spell_box.index, spell_box.index
                                return

                    return on_drag

                ui_state['spells_order'] = []

                for j, spell in enumerate(enchantments[i].spells):
                    if isinstance(spell, MoveSpell):
                        state.spell_boxes.append(MoveSpellButton(spell))
                        state.spell_boxes[-1].set_resource_mode(not isinstance(spell.destination, Position))
                    else:
                        state.spell_boxes.append(Button('ui_spell_box', 'ui_spell_box', 'ui_spell_box', generate_on_click_but_for_spell(j), True))

                    state.spell_boxes[-1].index = j
                    state.spell_boxes[-1].on_drag = generate_on_drag_still_for_spell(j, i)
                    ui_state['spells_order'].append(j)

                def on_click_retour():
                    spells = enchantments[ui_state['current_enchantment']].spells.copy()

                    for position, spell_index in enumerate(ui_state['spells_order']):
                        spells[position] = enchantments[ui_state['current_enchantment']].spells[spell_index]

                    enchantments[ui_state['current_enchantment']].spells = spells

                    ui_state['current_enchantment'] = None
                    ui_state['return_button'] = None

                    state.spell_boxes = []
                    generate_enchantments()

                ui_state['return_button'] = Button('ui_bouton_retour', 'ui_bouton_retour_hover', 'ui_bouton_retour_focus', on_click_retour)

                def on_click_add():
                    for spell in spells:
                        def generate_on_click(spell):
                            def on_click():
                                e = enchantments[ui_state['current_enchantment']]
                                index = len(e.spells)
                                e.spells.append(spell())

                                if isinstance(e.spells[-1], MoveSpell):
                                    state.spell_boxes.append(MoveSpellButton(e.spells[-1]))
                                    state.spell_boxes[-1].set_resource_mode(not isinstance(e.spells[-1].destination, Position))
                                else:
                                    state.spell_boxes.append(Button('ui_spell_box', 'ui_spell_box', 'ui_spell_box', generate_on_click_but_for_spell(index), True))

                                state.spell_boxes[-1].index = index
                                state.spell_boxes[-1].on_drag = generate_on_drag_still_for_spell(index, ui_state['current_enchantment'])
                                ui_state['spells_order'].append(index)

                                ui_state['window'] = False
                                ui_state['spell_buttons'] = []

                            return on_click

                        ui_state['spell_buttons'].append(Button('ui_spell_box', 'ui_spell_box', 'ui_spell_box', generate_on_click(spell)))

                    ui_state['window'] = True

                ui_state['add_button'] = Button('ui_enchantment_add', 'ui_enchantment_add_hover', 'ui_enchantment_add_focus', on_click_add)

                def on_click_quit():
                    ui_state['window'] = False
                    ui_state['spell_buttons'] = []

                ui_state['quit_button'] = Button('bouton_quitter', 'bouton_quitter_hover', 'bouton_quitter_focus', on_click_quit)

                ui_state['current_enchantment'] = i

            return on_click

        state.enchantment_boxes.append(Button('ui_enchantment_box', 'ui_enchantment_box_hover', 'ui_enchantment_box', generate_on_click(i)))

@window.event
def on_mouse_release(x, y, button, modifiers):
    mouse_position = Position(x, window.get_size()[1] - y)

    if button == pyglet.window.mouse.LEFT:
        if ui_state['tab_entities_focus']:
            ui_state['buy_button_slime'] = Button('acheter_slime', 'acheter_slime_hover', 'acheter_slime_focus', on_click_buy_slime)
            ui_state['buy_button_goblin'] = Button('acheter_goblin', 'acheter_goblin_hover', 'acheter_goblin_focus', on_click_buy_goblin)
            ui_state['buy_button_orc'] = Button('acheter_orc', 'acheter_orc_hover', 'acheter_slime_focus', on_click_buy_orc)
            ui_state['current_tab'] = 0
        elif ui_state['tab_enchantments_focus']:
            generate_enchantments()
            ui_state['current_tab'] = 1
        elif ui_state['tab_spells_focus']:
            ui_state['current_tab'] = 2
        elif ui_state['tab_settings_focus']:
            ui_state['current_tab'] = 3

        ui_state['tab_entities_focus'] = False
        ui_state['tab_enchantments_focus'] = False
        ui_state['tab_spells_focus'] = False
        ui_state['tab_settings_focus'] = False

        for button in buttons.copy():
            if button.focus:
                button.focus = False
                button.on_click()

scroll = 0

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global scroll

    scroll += scroll_y

    grid.zoom = 1.1 ** scroll

def update(dt):
    global entities

    for entity in entities:
        entity.update(dt)

    entities = list(filter(lambda entity: not entity.dead, entities))

    if len(entities) == 0 and state.wood_count < 20:
        ui_state['game_over'] = True

pyglet.clock.schedule_interval(update, 1/10)

if __name__ == '__main__':
    pyglet.app.run()
