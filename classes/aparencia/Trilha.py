from typing import Tuple

from ursina import *

quad = load_model('quad')


class Trilha(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.model = Mesh(vertices=[], uvs=[])

    def reset(self):
        self.model = Mesh(vertices=[], uvs=[])

    def nova_trilha(self, posicao: Tuple[int, int]):
        x, y = posicao

        self.model.vertices += [Vec3(*e) + Vec3(x + .5, y + .5, 0)
                                for e in quad.vertices]
        self.model.uvs += quad.uvs

        self.model.generate()
