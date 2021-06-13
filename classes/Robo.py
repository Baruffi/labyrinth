from typing import List, Tuple

from ursina import *
from ursina.hit_info import HitInfo

from classes.Caminho import Caminho

quad = load_model('quad')


class Robo(Entity):

    def __init__(self, caminho: Caminho, espera: float = 3, velocidade: int = 5):
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
        self.delta = 0

        self.objetivo = None
        self.posicao_objetivo = None

        self.caminho = caminho
        self.historia: List[Tuple[str, float]] = list()

    def reset(self):
        self.espera = self.espera_padrao

        self.direcao = Vec3(0, 0, 0).normalized()
        self.delta = 0

        self.objetivo = None
        self.posicao_objetivo = None

        self.caminho.reset()
        self.historia = list()

    def see(self):
        if self.objetivo:
            hit_info = boxcast(self.world_position, ignore=(
                self, self.objetivo, ), thickness=(2, 2), distance=2)

            return hit_info

    def find_objective(self):
        if self.objetivo and not self.posicao_objetivo:
            hit_info = self.lookup(self.up)

            if not hit_info.hit:
                hit_info = self.lookup(self.down)
            if not hit_info.hit:
                hit_info = self.lookup(self.left)
            if not hit_info.hit:
                hit_info = self.lookup(self.right)

            if hit_info.hit:
                self.posicao_objetivo = hit_info.world_point
                self.is_moving = True
                self.override_human = True

    def lookup(self, direcao: Vec3):
        return boxcast(self.world_position, direcao, traverse_target=self.objetivo, thickness=(self.scale_x * .8, self.scale_y * .8), distance=1)

    def canMove(self):
        hit_info = boxcast(self.world_position, self.direcao, ignore=(
            self,), thickness=(self.scale_x * .8, self.scale_y * .8), distance=self.scale_y / 2)

        return not hit_info.hit

    def move(self):
        self.position += self.direcao * self.delta * self.velocidade

    def get_rear(self):
        direcao_x = (self.world_x - (self.direcao.x / 2)) // 1
        direcao_y = (self.world_y - (self.direcao.y / 2)) // 1

        return direcao_x, direcao_y

    def update_direction(self):
        direcao_x, direcao_y = self.get_rear()
        sucesso = self.path_find(direcao_x, direcao_y)

        if not sucesso:
            print('Erro de pathfind!')

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

    def path_find(self, direcao_x, direcao_y):
        # print(direcao_x)
        # print(direcao_y)

        redor = self.caminho.getSurrounding((direcao_x, direcao_y))

        # print(redor)

        if redor['up'] == 'space':
            self.direcao = self.up.normalized()
            self.historia.append(('up', self.delta))
        elif redor['right'] == 'space':
            self.direcao = self.right.normalized()
            self.historia.append(('right', self.delta))
        elif redor['down'] == 'space':
            self.direcao = self.down.normalized()
            self.historia.append(('down', self.delta))
        elif redor['left'] == 'space':
            self.direcao = self.left.normalized()
            self.historia.append(('left', self.delta))
        else:
            if len(self.historia):
                ultima_direcao, delta = self.historia.pop()

                # print(ultima_direcao)

                if ultima_direcao == 'down':
                    self.direcao = self.up.normalized()
                elif ultima_direcao == 'left':
                    self.direcao = self.right.normalized()
                elif ultima_direcao == 'up':
                    self.direcao = self.down.normalized()
                elif ultima_direcao == 'right':
                    self.direcao = self.left.normalized()
                else:
                    return False

                self.delta = delta
            else:
                return False

        return True

    def memorizeHitinfo(self, hit_info: HitInfo):
        for entity in hit_info.entities:
            self.caminho.memorizeObstacle(
                (entity.world_x // 1, entity.world_y // 1))

    def memorizePath(self):
        direcao_x, direcao_y = self.get_rear()

        self.caminho.memorizePath((direcao_x, direcao_y))

    def update(self):
        self.delta = time.dt

        if self.espera > 0:
            self.espera -= self.delta
        else:
            self.find_objective()

            visao = self.see()

            if visao:
                self.memorizeHitinfo(visao)

            self.update_direction()

            if self.canMove():
                self.move()
                self.memorizePath()
