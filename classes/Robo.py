from ursina import *


class Robo():
    model = 'quad'
    color = color.lime
    scale = (0.3, 0.3)

    def __init__(self, *position: int):
        self.position = position
