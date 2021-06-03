from ursina import *


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
        self.direcao = None
        self.traverse_target = scene

    def reset(self):
        pass

    def move(self):
        self.position += self.direcao * time.dt * self.velocidade

    def update(self):
        self.direcao = None

        self.direcao = Vec3(
            self.up * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
        ).normalized()

        origin = self.world_position + Vec3(0, self.scale_y / 2, 0)
        hit_info = raycast(origin, self.direcao, ignore=(
            self,), distance=self.scale_y / 2)

        if not hit_info.hit:
            self.move()
