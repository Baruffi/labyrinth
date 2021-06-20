from ursina import *

from classes.Labirinto import Labirinto
from classes.Mapa import Mapa
from robos.exemplo.Exemplo import Exemplo

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

mapa.gerarDicionario(30)
labirinto.gerarVertices(mapa.dicionario)

inicio_x, inicio_y = mapa.inicio
posicao_inicial = Vec3(inicio_x + .5, inicio_y + .5, 0)
escala = Vec3(.5, .5, 0)
visao = Vec3(2, 2, 0)

robo = Exemplo(labirinto.fim, labirinto, posicao_inicial,
               escala, visao, espera=0, velocidade=100)


def reset():
    mapa.reset()
    labirinto.reset()

    mapa.gerarDicionario(30)
    labirinto.gerarVertices(mapa.dicionario)

    inicio_x, inicio_y = mapa.inicio
    posicao_inicial = Vec3(inicio_x + .5, inicio_y + .5, 0)

    robo.reset(labirinto.fim, labirinto, posicao_inicial)


def update():
    if held_keys['r']:
        reset()

    if robo.intersects(labirinto).hit:
        if robo.intersects(labirinto.fim).hit:
            reset()

    camera.world_x, camera.world_y = robo.world_x, robo.world_y


app.run()
