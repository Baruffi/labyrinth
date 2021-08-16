from typing import Tuple

from ursina import *


class Movimento():
    def __init__(self, obstaculo: Entity, ignorar: Tuple[Entity], velocidade: float, escala: Vec3):
        self.obstaculo = obstaculo
        self.ignorar = ignorar
        self.velocidade = velocidade
        self.escala = escala

    def edge_cast(self, posicao: Vec3, direcao: Vec3, espessura: Vec3, distancia: float):
        hit_info = boxcast(posicao, direcao, traverse_target=self.obstaculo,
                           ignore=self.ignorar, distance=distancia, thickness=espessura, debug=True)

        return hit_info

    def get_distancia_base(self, direcao: Vec3):
        distancia_base = sqrt(((self.escala.x / 2) * direcao.x)
                              ** 2 + ((self.escala.y / 2) * direcao.y) ** 2)

        return distancia_base

    def move(self, posicao: Vec3, direcao: Vec3, delta: float):
        distancia_base = self.get_distancia_base(direcao)
        hit_info = self.edge_cast(posicao, direcao, self.escala, distancia_base + (delta * self.velocidade))

        if hit_info.hit:
            if not hit_info.distance:
                return False

            stuck_hit_info = self.edge_cast(hit_info.point, direcao, self.escala, distancia_base)

            if stuck_hit_info.hit:
                return False

            return hit_info.point

        return posicao + direcao * delta * self.velocidade
