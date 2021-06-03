from typing import Dict, Tuple

from ursina import *

quad = load_model('quad')


class Labirinto(Entity):

    def __init__(self):
        super().__init__()
        self.texture = 'white_cube'
        self.model = Mesh(vertices=[], uvs=[])
        self.fim = None

    def reset(self):
        self.model = Mesh(vertices=[], uvs=[])
        self.fim = None

        [destroy(c) for c in self.children]

    def gerarVertices(self, dicionario: Dict[Tuple[int, int], str]):
        for posicao, tipo in dicionario.items():

            if tipo == 'start':
                Entity(parent=self, position=posicao, model='quad',
                       origin=(-.5, -.5), color=color.green)
            elif tipo == 'end':
                Entity(parent=self, position=posicao, model='quad',
                       origin=(-.5, -.5), color=color.red)

                self.fim = Entity(parent=self, position=posicao, model='quad',
                                  origin=(-.5, -.5), collider='box', visible=False)

                self.fim.scale = .5, .5
                self.fim.position = Vec3(self.fim.x + .25, self.fim.y + .25, 0)
            elif tipo == 'wall':
                x, y = posicao
                self.model.vertices += [Vec3(*e) + Vec3(x + .5, y + .5, 0)
                                        for e in quad.vertices]
                self.model.uvs += quad.uvs

                Entity(parent=self, position=posicao, model='quad',
                       origin=(-.5, -.5), collider='box', visible=False)

        self.model.generate()
