from typing import Dict, Tuple

from ursina import *

quad = load_model('quad')


class Caminho():

    def __init__(self):
        self.coordenadas: Dict[Tuple[int, int], str] = dict()

        self.path_entity = Entity(
            model=Mesh(vertices=[], uvs=[]), color=color.rgba(0, 128, 128, 100))
        self.obstacle_entity = Entity(
            model=Mesh(vertices=[], uvs=[]), color=color.rgba(128, 0, 128, 100), always_on_top=True)

    def reset(self):
        self.coordenadas = dict()

        self.path_entity.model = Mesh(vertices=[], uvs=[])
        self.obstacle_entity.model = Mesh(vertices=[], uvs=[])

    def memorizePath(self, path: Tuple[int, int]):
        if path not in self.coordenadas:
            x, y = path

            self.path_entity.model.vertices += [Vec3(*e) + Vec3(x + .5, y + .5, 0)
                                                for e in quad.vertices]
            self.path_entity.model.uvs += quad.uvs

            self.path_entity.model.generate()

        self.coordenadas[path] = 'path'

    def memorizeObstacle(self, obstacle: Tuple[int, int]):
        if obstacle not in self.coordenadas:
            x, y = obstacle

            self.obstacle_entity.model.vertices += [Vec3(*e) + Vec3(x + .5, y + .5, 0)
                                                    for e in quad.vertices]
            self.obstacle_entity.model.uvs += quad.uvs

            self.obstacle_entity.model.generate()

        self.coordenadas[obstacle] = 'obstacle'

    def getSurrounding(self, alvo: Tuple[int, int]):
        redor = dict.fromkeys(('right', 'left', 'up', 'down'), 'space')
        alvo_x, alvo_y = alvo

        for coordenada in self.coordenadas:
            x, y = coordenada

            if y == alvo_y and x <= alvo_x + 1 and x > alvo_x:
                redor['right'] = self.coordenadas[coordenada]

            if y == alvo_y and x < alvo_x and x >= alvo_x - 1:
                redor['left'] = self.coordenadas[coordenada]

            if x == alvo_x and y <= alvo_y + 1 and y > alvo_y:
                redor['up'] = self.coordenadas[coordenada]

            if x == alvo_x and y < alvo_y and y >= alvo_y - 1:
                redor['down'] = self.coordenadas[coordenada]

        return redor
