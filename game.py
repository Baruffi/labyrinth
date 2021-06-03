from ursina import *

from classes.Labirinto import Labirinto
from classes.Mapa import Mapa
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
mapa = Mapa()


def reset():
    labirinto.reset()
    robo.reset()
    mapa.reset()

    mapa.gerarDicionario(30)
    labirinto.gerarVertices(mapa.dicionario)

    inicio_x, inicio_y = mapa.inicio

    robo.position = inicio_x + .5, inicio_y + .5


def update():
    if robo.intersects(labirinto).hit:
        if robo.intersects(labirinto.fim).hit:
            reset()

    camera.world_x, camera.world_y = robo.world_x, robo.world_y


reset()

app.run()
