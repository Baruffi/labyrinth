from typing import Tuple

from ursina import *


class Caminho(Entity):

    def __init__(self, *pontos: Tuple[int, int, int]):
        super().__init__()
        self.model = Mesh(vertices=pontos, mode='line', thickness=2)
        self.color = 'black'
