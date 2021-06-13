from typing import List

from ursina import *
from ursina.hit_info import HitInfo

from classes.Caminho import Caminho

quad = load_model('quad')


class Robo(Entity):

    def __init__(self, caminho: Caminho, espera: float = 3, velocidade: int = 10):
        super().__init__()
        self.model = 'quad'
        self.color = color.blue
        self.scale = .5, .5
        self.collider = 'box'
        self.always_on_top = True

        self.espera_padrao = espera
        self.espera = espera
        self.velocidade = velocidade

        self.direcao = Vec3(0, 0, 0).normalized()
        self.is_moving = False

        self.objetivo = None
        self.posicao_objetivo = None
        self.override_human = False

        self.caminho = caminho
        self.history: List[str] = list()

    def reset(self):
        self.espera = self.espera_padrao

        self.direcao = Vec3(0, 0, 0).normalized()
        self.is_moving = False

        self.objetivo = None
        self.posicao_objetivo = None
        self.override_human = False

        self.caminho.reset()
        self.history = list()

    def see(self):
        if self.objetivo:
            hit_info = boxcast(self.world_position, ignore=(self, self.objetivo, ),
                               thickness=(2, 2), distance=2)

            return hit_info

    def findObjective(self):
        if self.objetivo and not self.posicao_objetivo:
            hit_info = boxcast(self.world_position, ignore=(
                self,), traverse_target=self.objetivo, thickness=(2, 2), distance=2)

            if hit_info.hit:
                self.posicao_objetivo = hit_info.world_point
                self.is_moving = True
                self.override_human = True

    def canMove(self):
        hit_info = boxcast(self.world_position, self.direcao, ignore=(
            self,), thickness=(self.scale_x * .8, self.scale_y * .8), distance=self.scale_y / 2)

        return not hit_info.hit

    def move(self):
        self.position += self.direcao * time.dt * self.velocidade

    def isMoving(self):
        if not self.override_human:
            if held_keys['w'] or held_keys['s'] or held_keys['d'] or held_keys['a']:
                self.is_moving = True
            else:
                self.is_moving = False

        return self.is_moving

    def getRear(self):
        direcao_x = (self.world_x - (self.direcao.x / 2)) // 1
        direcao_y = (self.world_y - (self.direcao.y / 2)) // 1

        return direcao_x, direcao_y

    def updateDirection(self):
        direcao_x, direcao_y = self.getRear()

        # print(direcao_x)
        # print(direcao_y)

        redor = self.caminho.getSurrounding((direcao_x, direcao_y))

        # print(redor)

        if redor['up'] == 'space':
            self.direcao = self.up.normalized()
            self.is_moving = True
            self.override_human = True
            self.history.append('up')
        elif redor['right'] == 'space':
            self.direcao = self.right.normalized()
            self.is_moving = True
            self.override_human = True
            self.history.append('right')
        elif redor['down'] == 'space':
            self.direcao = self.down.normalized()
            self.is_moving = True
            self.override_human = True
            self.history.append('down')
        elif redor['left'] == 'space':
            self.direcao = self.left.normalized()
            self.is_moving = True
            self.override_human = True
            self.history.append('left')
        else:
            ultima_direcao = self.history.pop()

            # print(ultima_direcao)

            if ultima_direcao == 'down':
                self.direcao = self.up.normalized()
                self.is_moving = True
                self.override_human = True
            elif ultima_direcao == 'left':
                self.direcao = self.right.normalized()
                self.is_moving = True
                self.override_human = True
            elif ultima_direcao == 'up':
                self.direcao = self.down.normalized()
                self.is_moving = True
                self.override_human = True
            elif ultima_direcao == 'right':
                self.direcao = self.left.normalized()
                self.is_moving = True
                self.override_human = True

        if self.posicao_objetivo:
            self.direcao = Vec3(
                self.down * (self.world_y - self.posicao_objetivo.y)
                + self.left * (self.world_x - self.posicao_objetivo.x)
            ).normalized()

        if held_keys['w'] or held_keys['s'] or held_keys['d'] or held_keys['a']:
            self.direcao = Vec3(
                self.up * (held_keys['w'] - held_keys['s'])
                + self.right * (held_keys['d'] - held_keys['a'])
            ).normalized()

    def memorizeHitinfo(self, hit_info: HitInfo):
        for entity in hit_info.entities:
            self.caminho.memorizeObstacle(
                (entity.world_x // 1, entity.world_y // 1))

    def memorizePath(self):
        direcao_x, direcao_y = self.getRear()

        self.caminho.memorizePath((direcao_x, direcao_y))

    def update(self):
        if self.espera > 0:
            self.espera -= time.dt
        else:
            self.findObjective()

            visao = self.see()

            if visao:
                self.memorizeHitinfo(visao)

            self.updateDirection()

            if self.canMove() and self.isMoving():
                self.move()
                self.memorizePath()
