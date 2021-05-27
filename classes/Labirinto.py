from typing import Tuple
from classes.Caminho import Caminho
from classes.Parede import Parede


class Labirinto():

    def __init__(self, paredes: Tuple[Parede], caminhos: Tuple[Caminho]):
        self.paredes = paredes
        self.caminhos = caminhos
