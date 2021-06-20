from typing import List, Tuple

from classes.aparencia.Parte import Parte
from classes.aparencia.Trilha import Trilha
from classes.comportamento.Memoria import Memoria
from classes.comportamento.Sensor import Sensor
from classes.Robo import Robo
from ursina import *

quad = load_model('quad')


class SelfAvoidingWalker(Robo):
    def __init__(self, alvo: Entity, obstaculo: Entity, posicao: Vec3, escala: Vec3, visao: Vec3, alcance=2, velocidade=5, espera=3):
        super().__init__(alvo, obstaculo, posicao, escala, velocidade, espera)

        self.color = color.light_gray

        self.direcoes = {
            'up': self.up, 'down': self.down, 'left': self.left, 'right': self.right}
        self.direcoes_reversas = {
            'up': self.down, 'down': self.up, 'left': self.right, 'right': self.left}

        self.historia: List[Tuple[str, float]] = list()

        self.sensor_obstaculos = Sensor(obstaculo, (alvo,), visao, alcance)
        self.sensor_objetivo = Sensor(alvo, (), escala, 1)
        self.memoria = Memoria()

        self.create_trails()
        self.create_parts()

    def create_trails(self):
        self.trilha_caminho = Trilha(color=color.rgba(0, 128, 128, 100))

        self.trilha_obstaculos = Trilha(
            color=color.rgba(128, 0, 128, 100), always_on_top=True)

    def create_parts(self):
        self.nariz_entity = Parte(self, Vec3(
            1, 0, 0), model='diamond', scale=(.5, .5), color=color.black, always_on_top=True)

        self.olho_esquerdo_entity = Parte(
            self, Vec3(.35, .35, 0), model='diamond', scale=(.6, .6), color=color.white, always_on_top=True)

        self.olho_direito_entity = Parte(
            self, Vec3(.35, -.35, 0), model='diamond', scale=(.6, .6), color=color.white, always_on_top=True)

        self.iris_esquerda_entity = Parte(
            self, Vec3(.4, .35, 0), model='diamond', scale=(.2, .2), color=color.black, always_on_top=True)

        self.iris_direita_entity = Parte(
            self, Vec3(.4, -.35, 0), model='diamond', scale=(.2, .2), color=color.black, always_on_top=True)

        self.cauda_entity = Parte(self, Vec3(-1, 0, 0), model=Mesh(
            vertices=[], uvs=[]), scale=(.4, .4), color=color.pink, always_on_top=True)

        self.cauda_entity.model.vertices += quad.vertices
        self.cauda_entity.model.uvs += quad.uvs

        self.cauda_entity.model.vertices += [Vec3(*e) + Vec3(.5, .5, 0)
                                             for e in quad.vertices]
        self.cauda_entity.model.uvs += quad.uvs

        self.cauda_entity.model.vertices += [Vec3(*e) + Vec3(1, 1, 0)
                                             for e in quad.vertices]
        self.cauda_entity.model.uvs += quad.uvs

        self.cauda_entity.model.generate()

    def reset(self, alvo: Entity, posicao: Vec3):
        super().reset(alvo, posicao)

        self.historia = list()

        self.memoria.reset()
        self.trilha_caminho.reset()
        self.trilha_obstaculos.reset()

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
            posicao = int(hit_info.world_point.x), int(hit_info.world_point.y)

            self.memoria.memorize(posicao, 'objective')

    def memorize_obstacles(self):
        hit_info = self.sensor_obstaculos.lookup(self.world_position)

        for entity in hit_info.entities:
            posicao = int(entity.world_x), int(entity.world_y)

            if posicao not in self.memoria.atual:
                self.trilha_obstaculos.nova_trilha(posicao)

            self.memoria.memorize(posicao, 'obstacle')

    def memorize_path(self):
        posicao = self.get_rear()

        if posicao not in self.memoria.atual:
            self.trilha_caminho.nova_trilha(posicao)

        self.memoria.memorize(posicao, 'path')

    def get_surrounding(self, alvo: Tuple[int, int]):
        redor = dict.fromkeys(('right', 'left', 'up', 'down'), 'space')
        alvo_x, alvo_y = alvo

        for coordenada in self.memoria.atual:
            x, y = coordenada

            if y == alvo_y and x <= alvo_x + 1 and x > alvo_x:
                redor['right'] = self.memoria.atual[coordenada]

            if y == alvo_y and x < alvo_x and x >= alvo_x - 1:
                redor['left'] = self.memoria.atual[coordenada]

            if x == alvo_x and y <= alvo_y + 1 and y > alvo_y:
                redor['up'] = self.memoria.atual[coordenada]

            if x == alvo_x and y < alvo_y and y >= alvo_y - 1:
                redor['down'] = self.memoria.atual[coordenada]

        return redor

    def path_find(self):
        posicao = self.get_rear()
        redor = self.get_surrounding(posicao)

        orientacao = next(iter([orientacao for orientacao in redor if redor[orientacao] == 'objective']), next(
            iter([orientacao for orientacao in redor if redor[orientacao] == 'space']), None))

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
        x_int = int(self.x)
        y_int = int(self.y)

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
