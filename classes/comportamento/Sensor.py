from typing import Tuple

from ursina import *


class Sensor():
    def __init__(self, alvo: Entity, ignorar: Tuple[Entity], escala: Vec3, distancia: float):
        self.alvo = alvo
        self.ignorar = ignorar
        self.escala = escala
        self.distancia = distancia

    def lookup(self, posicao: Vec3, direcao: Vec3 = Vec3(0, 0, 0)):
        return boxcast(posicao, direcao, traverse_target=self.alvo, ignore=self.ignorar, thickness=self.escala, distance=self.distancia)
