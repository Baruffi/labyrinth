from ursina import *


class Robo(Entity):

    def __init__(self, *position: int):
        super().__init__()
        self.model = 'quad'
        self.color = color.lime
        self.scale = (0.3, 0.3)
        self.collider = 'box'
        self.position = position

    def update(self):
        if held_keys['w']:
            self.position += self.up * 0.2
        if held_keys['a']:
            self.position += self.left * 0.2
        if held_keys['d']:
            self.position += self.right * 0.2
        if held_keys['s']:
            self.position += self.down * 0.2
