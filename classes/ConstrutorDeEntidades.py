from typing import List

from ursina import *

from classes.Labirinto import Labirinto
from classes.Parede import Parede
from classes.Robo import Robo


class ConstrutorDeEntidades():

    def construirRobo(self, robo: Robo):
        return Entity(model=robo.model, color=robo.color, position=robo.position, scale=robo.scale)

    def construirParede(self, parede: Parede):
        return Entity(model=parede.mesh)

    def construirLabirinto(self, labirinto: Labirinto) -> List[Entity]:
        entidades = []

        for parede in labirinto.paredes:
            entidades.append(Entity(model=parede.mesh))

        return entidades
