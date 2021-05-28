from ursina import *


class Robo(Entity):

    def __init__(self, *position: int):
        super().__init__()
        self.model = 'quad'
        self.color = color.lime
        self.scale = .5, .5
        self.origin_y = -.5
        self.collider = 'box'
        self.position = position
        self.velocidade = 10

    def update(self):
        if held_keys['w']:
            self.position += self.up * time.dt * self.velocidade
        if held_keys['a']:
            self.position += self.left * time.dt * self.velocidade
        if held_keys['d']:
            self.position += self.right * time.dt * self.velocidade
        if held_keys['s']:
            self.position += self.down * time.dt * self.velocidade
