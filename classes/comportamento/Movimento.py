from typing import Tuple

from ursina import *


class Movimento():
    def __init__(self, obstaculo: Entity, ignorar: Tuple[Entity], velocidade: float, escala: Vec3):
        self.obstaculo = obstaculo
        self.ignorar = ignorar
        self.velocidade = velocidade
        self.escala = escala

    def can_move(self, posicao: Vec3, direcao: Vec3):
        hit_info = boxcast(posicao, direcao, traverse_target=self.obstaculo,
                           ignore=self.ignorar, thickness=self.escala * .8, distance=(self.escala.y / 2))

        return not hit_info.hit

    def move(self, posicao: Vec3, direcao: Vec3, delta: float):
        hit_info = boxcast(posicao, direcao, traverse_target=self.obstaculo, ignore=self.ignorar,
                           thickness=self.escala * .8, distance=(self.escala.y / 2) + (delta * self.velocidade))

        if hit_info.hit:
            if direcao.x:
                return Vec3(hit_info.world_point.x - direcao.x * self.escala.y / 2, posicao.y, 0)
            elif direcao.y:
                return Vec3(posicao.x, hit_info.world_point.y - direcao.y * self.escala.y / 2, 0)
        else:
            return posicao + direcao * delta * self.velocidade
