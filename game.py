from ursina import *

from classes.ConstrutorDeEntidades import ConstrutorDeEntidades
from classes.ControladorRobo import ControladorRobo
from classes.Labirinto import Labirinto
from classes.Parede import Parede
from classes.Robo import Robo

construtor = ConstrutorDeEntidades()

robo = Robo(0, 0)
parede1 = Parede((0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0))
parede2 = Parede((3, 0, 0), (3, 1, 0), (4, 1, 0), (4, 2, 0))
labirinto = Labirinto(parede1, parede2)

entidadesLabirinto = construtor.construirLabirinto(labirinto)
entidadeRobo = construtor.construirRobo(robo)

controlador = ControladorRobo(entidadeRobo)


def update():
    controlador.atualizar()


app = Ursina()

window.title = 'Labirinto'                # The window title
window.borderless = False               # Show a border
window.fullscreen = False               # Do not go Fullscreen
# Do not show the in-game red X that loses the window
window.exit_button.visible = False
# Show the FPS (Frames per second) counter
window.fps_counter.enabled = True

app.run()                               # Run the app
