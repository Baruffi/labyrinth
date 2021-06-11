from ursina import *
from ursina.hit_info import HitInfo


class Robo(Entity):

    def __init__(self, *position: int):
        super().__init__()
        self.model = 'quad'
        self.color = color.blue
        self.scale = .5, .5
        self.origin_y = -.5
        self.collider = 'box'
        self.position = position
        self.velocidade = 10
        self.sentido = 1
        self.direcao = Vec3(0, 0, 0).normalized()
        self.is_moving = False
        self.mapa_construido = set()
        self.objetivo = None
        self.posicao_objetivo = None
        self.override_human = False

    def reset(self):
        self.direcao = Vec3(0, 0, 0).normalized()
        self.is_moving = False
        self.mapa_construido = set()
        self.objetivo = None
        self.posicao_objetivo = None
        self.override_human = False

    def getOrigin(self):
        return self.world_position + Vec3(0, self.scale_y / 2, 0)

    def see(self):
        if self.objetivo:
            hit_info = boxcast(self.getOrigin(), ignore=(self, self.objetivo, ),
                               thickness=(2.5, 2.5), distance=2.5, debug=True)

            return hit_info

    def findObjective(self):
        if self.objetivo and not self.posicao_objetivo:
            hit_info = boxcast(self.getOrigin(), ignore=(
                self,), traverse_target=self.objetivo, thickness=(2.5, 2.5), distance=2.5, debug=True)

            if hit_info.hit:
                self.posicao_objetivo = hit_info.world_point
                self.is_moving = True
                self.override_human = True

    def moveToObjective(self):
        if self.posicao_objetivo:
            self.direcao = Vec3(
                self.down * (self.world_y - self.posicao_objetivo.y)
                + self.left * (self.world_x - self.posicao_objetivo.x)
            ).normalized()

    def memorizeHitinfo(self, hit_info: HitInfo):
        self.mapa_construido.union(hit_info.hits)

    def canMove(self):
        hit_info = raycast(self.getOrigin(), self.direcao, ignore=(
            self,), distance=self.scale_y / 2)

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

    def updateDirection(self):
        if held_keys['w'] or held_keys['s'] or held_keys['d'] or held_keys['a']:
            self.direcao = Vec3(
                self.up * (held_keys['w'] - held_keys['s'])
                + self.right * (held_keys['d'] - held_keys['a'])
            ).normalized()

        self.direcao = self.direcao * self.sentido

    def tweakDirection(self):
        hit_info = raycast(self.getOrigin(), self.direcao, ignore=(
            self,), distance=self.scale_y / 2)

        self.direcao = Vec3(
            self.up * (hit_info.world_normal.x)
            + self.right * (hit_info.world_normal.y)
        ).normalized()

    def update(self):
        self.findObjective()
        self.moveToObjective()

        visao = self.see()

        if visao:
            self.memorizeHitinfo(visao)

        self.updateDirection()

        self.move_cycle(50)

    def move_cycle(self, depth: int):
        if depth == 0:
            self.sentido = - self.sentido
            return

        if self.isMoving():
            if self.canMove():
                self.move()
            else:
                self.tweakDirection()
                self.move_cycle(depth - 1)
