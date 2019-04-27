import pyglet
from os import listdir
from os.path import isfile, join

files = [f for f in listdir('resources') if isfile(join('resources', f))]

def update_anchor(image):
    image.anchor_y = image.height

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

images = {}

for file in files:
    if file[-4:] == '.png':
        images[file[:-4]] = pyglet.resource.image(file)
        update_anchor(images[file[:-4]])
