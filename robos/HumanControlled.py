from classes.aparencia.Trilha import Trilha
from classes.comportamento.Memoria import Memoria
from classes.Robo import Robo
from ursina import *


class HumanControlled(Robo):
    def __init__(self, alvo: Entity, obstaculo: Entity, posicao: Vec3, escala: Vec3, velocidade=5, espera=3):
        super().__init__(alvo, obstaculo, posicao, escala, velocidade, espera)

        self.color = color.blue

        self.memoria = Memoria()
        self.trilha_caminho = Trilha(color=color.rgba(0, 128, 128, 100))

    def reset(self, alvo: Entity, posicao: Vec3):
        super().reset(alvo, posicao)

        self.memoria.reset()
        self.trilha_caminho.reset()

    def update_direction(self):
        if held_keys['w'] or held_keys['s'] or held_keys['d'] or held_keys['a']:
            self.orientacao = Vec3(
                self.up * (held_keys['w'] - held_keys['s'])
                + self.right * (held_keys['d'] - held_keys['a'])
            ).normalized()

    def memorize_path(self):
        posicao = self.get_rear()

        if posicao not in self.memoria.atual:
            self.trilha_caminho.nova_trilha(posicao)

        self.memoria.memorize(posicao, 'path')

    def pre_move(self):
        self.update_direction()

    def post_move(self):
        self.memorize_path()
