import itertools
import random


class Mapa():

    def __init__(self):
        self.dicionario = {}
        self.inicio = (0, 0)
        self.fim = (0, 0)

    def reset(self):
        self.dicionario = {}
        self.inicio = (0, 0)
        self.fim = (0, 0)

    def gerarDicionario(self, numero_de_linhas: int):
        rows = range(numero_de_linhas)
        def rect(*sides): return {j-i*1j for i, j in itertools.product(*sides)}
        def coord(z): return (int(z.real), -int(z.imag))
        def pick(iterable): return random.choice(list(iterable))
        maze, seen, reseen = dict.fromkeys(
            rect(rows, rows), 'wall'), set(), set()
        pos = pick(maze)

        maze[pos] = 'start'

        while ...:
            ways = {d for d in (1, 1j, -1, -1j) if all(maze.get(pos+d*t) == 'wall'
                    for t in rect({-1, 0, 1}, {1, 2}) - {1})}
            if ways:
                pos += pick(ways)
                seen.add(pos)
                if maze[pos] == 'wall':
                    maze[pos] = 'free'
            elif seen:
                pos = seen.pop()
                reseen.add(pos)
            else:
                if len(reseen or seen) == 0:
                    return self.gerarDicionario(numero_de_linhas)
                else:
                    break

        maze[pick(reseen or seen)] = 'end'

        for posicao, tipo in maze.items():
            if tipo == 'start':
                self.inicio = coord(posicao)
            elif tipo == 'end':
                self.fim = coord(posicao)

            self.dicionario[coord(posicao)] = tipo
