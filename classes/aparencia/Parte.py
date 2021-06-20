from classes.aparencia.Corpo import Corpo
from ursina import *


class Parte(Entity):
    def __init__(self, parent: Corpo, posicao_inicial: Vec3 = Vec3(0, 0, 0), **kwargs):
        super().__init__(**kwargs)

        self.parent: Corpo = parent
        self.position = posicao_inicial

        # TODO: ver se precisa de copia aqui também
        self.posicao_inicial = posicao_inicial

    def reset(self):
        self.position = self.posicao_inicial

    def update(self):
        self.position = Vec3(self.parent.orientacao.x * self.posicao_inicial.x + self.parent.orientacao.y * self.posicao_inicial.y,
                             self.parent.orientacao.y * self.posicao_inicial.x + self.parent.orientacao.x * self.posicao_inicial.y, 0)
