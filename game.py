from ursina import *

from classes.Labirinto import Labirinto
from classes.Robo import Robo

window.vsync = False

app = Ursina()

window.title = 'Labirinto'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

camera.orthographic = True
camera.fov = 24

robo = Robo(0, 0)
labirinto = Labirinto()

labirinto.gerarVertices(10, 10)


def update():
    if robo.intersects(labirinto).hit:
        print('colisao')

    camera.world_x, camera.world_y = robo.world_x, robo.world_y


app.run()
