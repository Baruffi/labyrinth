import random

from ursina import *

quads = [Entity(model='quad', color=color.orange, scale=(2, 2), position=(0, 0)), Entity(
    model='quad', color=color.orange, scale=(3, 1), position=(2, 1)), Entity(model='quad', color=color.orange, scale=(1, 3), position=(-1, -2))]

random_generator = random.Random()


def update():
    for quad in quads:
        updateQuad(quad)


def updateQuad(quad: Entity):
    # quad.rotation_y += time.dt * 100
    if held_keys['r']:
        red = random_generator.random() * 255
        green = random_generator.random() * 255
        blue = random_generator.random() * 255
        quad.color = color.rgb(red, green, blue)


app = Ursina()

window.title = 'My Game'                # The window title
window.borderless = False               # Show a border
window.fullscreen = False               # Do not go Fullscreen
# Do not show the in-game red X that loses the window
window.exit_button.visible = False
# Show the FPS (Frames per second) counter
window.fps_counter.enabled = True

app.run()                               # Run the app
