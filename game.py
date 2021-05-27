from ursina import *

from classes.Labirinto import Labirinto
from classes.Parede import Parede
from classes.Robo import Robo

robo = Robo(0, 0)
parede1 = Parede((0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0))
parede2 = Parede((3, 0, 0), (3, 1, 0), (4, 1, 0), (4, 2, 0))
labirinto = Labirinto((parede1, parede2), ())


def update():
    for parede in labirinto.paredes:
        if robo.intersects(parede).hit:
            print('colisao')

    camera.world_x, camera.world_y = robo.world_x, robo.world_y


app = Ursina()

window.title = 'Labirinto'                # The window title
window.borderless = False               # Show a border
window.fullscreen = False               # Do not go Fullscreen
# Do not show the in-game red X that loses the window
window.exit_button.visible = False
# Show the FPS (Frames per second) counter
window.fps_counter.enabled = True

camera.orthographic = True
camera.fov = 16

app.run()                               # Run the app
