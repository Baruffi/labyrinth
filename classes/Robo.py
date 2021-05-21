from ursina import *


class Robo():
    model = 'quad'
    color = color.orange

    def __init__(self, *position: int):
        self.position = position
