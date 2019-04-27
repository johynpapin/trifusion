import pyglet

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

grass_image = pyglet.resource.image('grass.png')
