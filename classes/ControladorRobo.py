from ursina import *


class ControladorRobo():

    def __init__(self, entidadeRobo: Entity):
        self.robo = entidadeRobo

    def atualizar(self):
        if held_keys['w']:
            self.robo.position += self.robo.up * 0.1
        if held_keys['a']:
            self.robo.position += self.robo.left * 0.1
        if held_keys['d']:
            self.robo.position += self.robo.right * 0.1
        if held_keys['s']:
            self.robo.position += self.robo.down * 0.1
