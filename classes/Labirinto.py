from random import randint

from ursina import *

quad = load_model('quad')


class Labirinto(Entity):

    def __init__(self):
        super().__init__()
        self.model = Mesh(vertices=[], uvs=[])
        self.texture = 'white_cube'

    def gerarVertices(self, largura: int, altura: int):
        [destroy(c) for c in self.children]

        for y in range(altura):
            collider = None

            for x in range(largura):
                isWall = randint(0, 1)

                if isWall:
                    self.model.vertices += [Vec3(*e) + Vec3(x+.5, y+.5, 0)
                                            for e in quad.vertices]
                    self.model.uvs += quad.uvs

                    if not collider:
                        collider = Entity(parent=self, position=(
                            x, y), model='quad', origin=(-.5, -.5), collider='box', visible=False)
                    else:
                        collider.scale_x += 1
                else:
                    collider = None

        self.model.generate()
