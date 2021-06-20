from copy import copy
from typing import Dict


class Memoria():
    def __init__(self, inicial: Dict = dict()):
        # TODO: verificar por que precisa fazer copia aqui
        self.inicial = inicial
        self.atual = copy(inicial)

    def reset(self):
        self.atual = copy(self.inicial)

    def memorize(self, objeto, estado):
        self.atual[objeto] = estado
