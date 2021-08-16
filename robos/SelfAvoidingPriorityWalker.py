from operator import itemgetter
from typing import Dict, List, Tuple

from classes.aparencia.Trilha import Trilha
from classes.comportamento.Memoria import Memoria
from classes.comportamento.Sensor import Sensor
from classes.Robo import Robo
from ursina import *

quad = load_model('quad')


class SelfAvoidingPriorityWalker(Robo):
    def __init__(self, alvo: Entity, obstaculo: Entity, posicao: Vec3, escala: Vec3, alcance=2, velocidade=5, espera=3, color: Color = color.cyan, reverse=False):
        super().__init__(alvo, obstaculo, posicao, escala, velocidade, espera)

        self.color = color

        self.alcance = alcance
        self.reverse = reverse

        self.direcoes = {
            'up': self.up, 'down': self.down, 'left': self.left, 'right': self.right}
        self.direcoes_reversas = {
            'up': self.down, 'down': self.up, 'left': self.right, 'right': self.left}

        self.historia: List[Tuple[str, float]] = list()

        self.sensor_obstaculos = Sensor(obstaculo, (alvo,), escala, alcance)
        self.sensor_objetivo = Sensor(alvo, (), escala, alcance)
        self.memoria = Memoria()

        self.create_trails()

    def create_trails(self):
        self.trilha_caminho = Trilha(color=color.rgba(0, 0, 128, 100))

        self.trilha_obstaculos = Trilha(
            color=color.rgba(128, 0, 0, 100), always_on_top=True)

        self.trilha_espacos = Trilha(color=color.rgba(0, 128, 0, 100))

    def reset(self, alvo: Entity, posicao: Vec3):
        super().reset(alvo, posicao)

        self.historia = list()

        self.memoria.reset()
        self.trilha_caminho.reset()
        self.trilha_obstaculos.reset()
        self.trilha_espacos.reset()

        self.sensor_obstaculos.ignorar = (alvo,)
        self.sensor_objetivo.alvo = alvo

    def memorize_objective(self):
        hit_info = self.sensor_objetivo.lookup(self.world_position, self.up)

        if not hit_info.hit:
            hit_info = self.sensor_objetivo.lookup(
                self.world_position, self.right)
        if not hit_info.hit:
            hit_info = self.sensor_objetivo.lookup(
                self.world_position, self.down)
        if not hit_info.hit:
            hit_info = self.sensor_objetivo.lookup(
                self.world_position, self.left)

        if hit_info.hit:
            posicao = floor(hit_info.world_point.x), floor(hit_info.world_point.y)

            self.memoria.memorize(posicao, 'objective')

    def memorize_obstacles(self):
        for direcao in self.direcoes.values():
            direcao = Vec3(*direcao.normalized())

            hit_info = self.sensor_obstaculos.lookup(self.world_position, direcao)

            if hit_info.distance > 1:
                for quadro in range(1, round(hit_info.distance)):
                    posicao_espaco = self.world_position + (quadro * direcao)
                    posicao_espaco = floor(posicao_espaco.x), floor(posicao_espaco.y)

                    if posicao_espaco not in self.memoria.atual:
                        self.trilha_espacos.nova_trilha(posicao_espaco)
                        self.memoria.memorize(posicao_espaco, 'space')

            if hit_info.hit and hit_info.world_point:
                posicao_parede = floor(hit_info.world_point.x), floor(hit_info.world_point.y)

                if posicao_parede not in self.memoria.atual:
                    self.trilha_obstaculos.nova_trilha(posicao_parede)
                    self.memoria.memorize(posicao_parede, 'obstacle')

    def memorize_path(self):
        posicao = self.get_rear()

        if posicao not in self.memoria.atual or self.memoria.atual[posicao] == 'space':
            self.trilha_caminho.nova_trilha(posicao)
            self.memoria.memorize(posicao, 'path')

    def get_surrounding(self):
        redor = dict.fromkeys(('right', 'left', 'up', 'down'), {})
        origem_x, origem_y = self.get_rear()

        # counter = 1
        # while ...:
        #     posicao = (origem_x + counter, origem_y)
        #     if posicao in self.memoria.atual:
        #         redor['right'][counter] = self.memoria.atual[posicao]
        #         break
        #     else:
        #         pass

        # print(f'{self.memoria.atual=}')

        for coordenada in self.memoria.atual:
            x, y = coordenada

            if y == origem_y and x > origem_x:
                redor['right'] = {**redor['right'],
                                  abs(x - origem_x): self.memoria.atual[coordenada]}

            if y == origem_y and x < origem_x:
                redor['left'] = {**redor['left'],
                                 abs(x - origem_x): self.memoria.atual[coordenada]}

            if x == origem_x and y > origem_y:
                redor['up'] = {**redor['up'],
                               abs(y - origem_y): self.memoria.atual[coordenada]}

            if x == origem_x and y < origem_y:
                redor['down'] = {**redor['down'],
                                 abs(y - origem_y): self.memoria.atual[coordenada]}

        return redor

    def get_path(self, redor: Dict[str, Dict[int, str]], caminhos_viaveis: Dict[str, List[int]]):
        for caminho in caminhos_viaveis:
            if any([passo for passo in caminhos_viaveis[caminho] if redor[caminho][passo] == 'objective']):
                return caminho

        caminhos_viaveis_ordenados = sorted(
            [(caminho, *caminhos_viaveis[caminho]) for caminho in caminhos_viaveis], key=len, reverse=self.reverse)

        if (caminho_viavel := next(iter(caminhos_viaveis_ordenados), None)):
            return next(iter(caminho_viavel))

    def path_find(self):
        redor = self.get_surrounding()
        caminhos_viaveis = {}

        for caminho in redor:
            caminho_viavel = []

            for passo in redor[caminho]:
                if redor[caminho][passo] not in ('path', 'obstacle'):
                    caminho_viavel.append(passo)
                else:
                    break

            if caminho_viavel:
                caminhos_viaveis[caminho] = caminho_viavel

        # print(f'{redor=}', f'{caminhos_viaveis=}')

        orientacao = self.get_path(redor, caminhos_viaveis)

        if orientacao:
            self.orientacao = self.direcoes[orientacao].normalized()
            self.historia.append((orientacao, self.delta))
        else:
            ultima_orientacao, delta = self.historia.pop()

            self.orientacao = self.direcoes_reversas[ultima_orientacao].normalized(
            )
            self.delta = delta

    def update_direction(self):
        try:
            self.path_find()
        except Exception as e:
            print(f'Erro de pathfind: {e!r}')

    def ajust_center(self):
        x_int = floor(self.x)
        y_int = floor(self.y)

        if not self.orientacao.x:
            self.x = x_int + .5
        if not self.orientacao.y:
            self.y = y_int + .5

    def pre_move(self):
        self.memorize_objective()
        self.memorize_obstacles()

        self.update_direction()

    def post_move(self):
        self.ajust_center()
        self.memorize_path()
