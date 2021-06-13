from ursina import *

from classes.Caminho import Caminho
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

mapa = Mapa()
labirinto = Labirinto()
caminho = Caminho()
robo = Robo(caminho)


def reset():
    mapa.reset()
    labirinto.reset()

    mapa.gerarDicionario(30)
    labirinto.gerarVertices(mapa.dicionario)

    robo.reset()

    inicio_x, inicio_y = mapa.inicio

    robo.position = inicio_x + .5, inicio_y + .5
    robo.objetivo = labirinto.fim


def update():
    if held_keys['r']:
        reset()

    if robo.intersects(labirinto).hit:
        if robo.intersects(labirinto.fim).hit:
            reset()

    camera.world_x, camera.world_y = robo.world_x, robo.world_y


reset()

app.run()
