import pyglet

def update_anchor(image):
    image.anchor_y = image.height

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

ui_header_image = pyglet.resource.image('ui_header.png')
update_anchor(ui_header_image)

ui_footer_image = pyglet.resource.image('ui_footer.png')
update_anchor(ui_footer_image)

ui_background_image = pyglet.resource.image('ui_background.png')
update_anchor(ui_background_image)

grass_image = pyglet.resource.image('grass.png')
update_anchor(grass_image)

slime_front_left_image = pyglet.resource.image('slime_front_left.png')
update_anchor(slime_front_left_image)

slime_front_left_crushed_image = pyglet.resource.image('slime_front_left_crushed.png')
update_anchor(slime_front_left_crushed_image)
