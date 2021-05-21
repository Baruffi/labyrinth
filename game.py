from ursina import *

from classes.ConstrutorDeEntidades import ConstrutorDeEntidades
from classes.Labirinto import Labirinto
from classes.Parede import Parede
from classes.Robo import Robo

construtor = ConstrutorDeEntidades()

robo = Robo(0, 0)
parede = Parede((0, 0, 0), (1, 0, 0))
labirinto = Labirinto(parede)

entidadesLabirinto = construtor.construirLabirinto(labirinto)
entidadeRobo = construtor.construirRobo(robo)


def update():
    pass


app = Ursina()

window.title = 'Labirinto'                # The window title
window.borderless = False               # Show a border
window.fullscreen = False               # Do not go Fullscreen
# Do not show the in-game red X that loses the window
window.exit_button.visible = False
# Show the FPS (Frames per second) counter
window.fps_counter.enabled = True

app.run()                               # Run the app
