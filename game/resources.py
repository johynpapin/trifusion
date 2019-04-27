import pyglet

def update_anchor(image):
    image.anchor_y = image.height

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

grass_image = pyglet.resource.image('grass.png')
update_anchor(grass_image)

slime_front_left_image = pyglet.resource.image('slime_front_left.png')
update_anchor(slime_front_left_image)

slime_front_left_crushed_image = pyglet.resource.image('slime_front_left_crushed.png')
update_anchor(slime_front_left_crushed_image)
