from typing import Tuple

from ursina import *


class Parede():

    def __init__(self, *pontos: Tuple[int, int, int]):
        self.mesh = Mesh(vertices=pontos, mode='line')

    def entity(self):
        Entity(model=self.mesh)
