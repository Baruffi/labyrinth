from collections import deque
from typing import Deque

from ursina import *

from classes.Labirinto import Labirinto
from classes.Mapa import Mapa
from classes.Robo import Robo
from robos.HumanControlled import HumanControlled
from robos.SelfAvoidingPriorityWalker import SelfAvoidingPriorityWalker
from robos.SelfAvoidingWalker import SelfAvoidingWalker

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
alcance = 2
espera = 0
velocidade = 50

human_controlled = HumanControlled(
    labirinto.fim, labirinto, posicao_inicial, escala, velocidade, espera)
self_avoiding_walker = SelfAvoidingWalker(
    labirinto.fim, labirinto, posicao_inicial, escala, visao, alcance, velocidade, espera)
# self_avoiding_priority_walker = SelfAvoidingPriorityWalker(
#     labirinto.fim, labirinto, posicao_inicial, escala, alcance, velocidade, espera)
# self_avoiding_priority_walker_reversed = SelfAvoidingPriorityWalker(
#     labirinto.fim, labirinto, posicao_inicial, escala, alcance, velocidade, espera, color.turquoise, True)

robos: Deque[Robo] = deque(
    [human_controlled, self_avoiding_walker]
)


def reset():
    mapa.reset()
    labirinto.reset()

    mapa.gerarDicionario(30)
    labirinto.gerarVertices(mapa.dicionario)

    inicio_x, inicio_y = mapa.inicio
    posicao_inicial = Vec3(inicio_x + .5, inicio_y + .5, 0)

    for robo in robos:
        robo.reset(labirinto.fim, posicao_inicial)


def update():
    if held_keys['r']:
        reset()

    if held_keys['q']:
        robos.rotate(-1)

    if held_keys['e']:
        robo = robos.rotate(1)

    concluiram_o_labirinto = [
        robo for robo in robos if robo.intersects(labirinto.fim).hit]

    for robo in concluiram_o_labirinto:
        robo.espera = 1000

    if len(concluiram_o_labirinto) == len(robos):
        reset()

    robo = robos[0]

    camera.world_x, camera.world_y = robo.world_x, robo.world_y


app.run()
