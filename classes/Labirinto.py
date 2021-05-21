from classes.Parede import Parede


class Labirinto():

    def __init__(self, *paredes: Parede):
        self.paredes = paredes
