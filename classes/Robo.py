from ursina import *

from classes.aparencia.Corpo import Corpo
from classes.comportamento.Movimento import Movimento


class Robo(Corpo):
    def __init__(self, alvo: Entity, obstaculo: Entity, posicao: Vec3, escala: Vec3, velocidade=5, espera=3):
        super().__init__(Vec3(0, 0, 0))
        self.model = 'quad'
        self.collider = 'box'
        self.always_on_top = True
        self.position = posicao
        self.scale = escala

        self.espera_padrao = espera
        self.espera = espera
        self.delta = 0

        self.obstaculo = obstaculo
        self.movimento = Movimento(obstaculo, (alvo,), velocidade, escala)

    def reset(self, alvo: Entity, posicao: Vec3):
        super().reset()

        self.espera = self.espera_padrao
        self.delta = 0

        self.movimento.ignorar = (alvo,)
        self.position = posicao

    def get_rear(self):
        # TODO: verificar se 2.1 é o melhor número
        x = floor(self.world_x - (self.orientacao.x / 2.1))
        y = floor(self.world_y - (self.orientacao.y / 2.1))

        return x, y

    def is_moving(self):
        return bool(self.orientacao.x or self.orientacao.y)

    def pre_move(self):
        pass

    def move(self):
        nova_posicao = self.movimento.move(self.position, self.orientacao, self.delta)

        return nova_posicao

    def post_move(self):
        pass

    def update_delta(self):
        self.delta = time.dt

    def update(self):
        self.update_delta()

        if self.delta * self.movimento.velocidade > 1:
            return

        if self.espera > 0:
            self.espera -= self.delta
        else:
            self.pre_move()

            if self.is_moving() and (nova_posicao := self.move()):
                self.position = nova_posicao
                self.post_move()
