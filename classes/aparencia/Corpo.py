from typing import Union

from ursina import *


class Corpo(Entity):
    def __init__(self, orientacao_inicial: Vec3, **kwargs):
        super().__init__(**kwargs)

        self.orientacao = orientacao_inicial
        self.orientacao_inicial = orientacao_inicial

    def reset(self):
        self.orientacao = self.orientacao_inicial
