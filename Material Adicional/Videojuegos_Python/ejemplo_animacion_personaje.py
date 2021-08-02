
from pyglet.window import key
from pyglet.image import load, ImageGrid
from cocos.director import director
from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.euclid import Vector2
from collections import defaultdict

class MiObjeto(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image)
        self.position = (x, y)

    def move(self, offset):
        self.position += offset

    def update(self, delta_t):
        pass


class MiPersonaje(MiObjeto):
    TECLAS_PULSADAS = defaultdict(int)
    pulsado = False

    def __init__(self,imagen, x, y):
        super().__init__(imagen, x, y)
        self.velocidad = Vector2(400, 0)

    def update(self, delta_t):
        pulsadas = MiPersonaje.TECLAS_PULSADAS

        movimiento = pulsadas[key.RIGHT] - pulsadas[key.LEFT]
        if movimiento != 0:
            delta_x = (self.velocidad * movimiento * delta_t)[0]
            if self.x  <= self.parent.ancho_ventana - self.width/5 - delta_x:
                if self.x - self.width/5 + delta_x > abs(delta_x):
                    self.move(self.velocidad * movimiento * delta_t)

        if pulsadas[key.RIGHT] and not self.pulsado:
            self.pulsado = True
            self.image = mi_animacion
        if pulsadas[key.LEFT] and not self.pulsado:
            self.pulsado = True
            self.image = mi_animacion2
        if not pulsadas[key.RIGHT] and not pulsadas[key.LEFT]:
            self.image = load('fotograma_base.png')
            self.pulsado = False


class MiCapa(ColorLayer):
    is_event_handler = True

    def __init__(self):
        super().__init__(0, 150, 255, 255)
        global mi_animacion, mi_animacion2
        self.ancho_ventana, _ = director.get_window_size()

        mi_secuencia = ImageGrid(load('fotogramas_dcha.png'), 2, 2)
        mi_secuencia2 = ImageGrid(load('fotogramas_izqda.png'), 2, 2)
        mi_animacion = mi_secuencia.get_animation(0.2)
        mi_animacion2 = mi_secuencia2.get_animation(0.2)

        self.personaje = MiPersonaje(mi_animacion, self.ancho_ventana * 0.5, 250)
        self.add(self.personaje)
        self.schedule(self.update)

    def on_key_press(self, k, _):
        MiPersonaje.TECLAS_PULSADAS[k] = 1

    def on_key_release(self, k, _):
        MiPersonaje.TECLAS_PULSADAS[k] = 0

    def update(self, dt):
        self.children[0][1].update(dt)


if __name__ == '__main__':
    ventana = director.init(caption='Animación del personaje',
                            width=1600, height=800)
    ventana.set_location(150,100)
    director.run(Scene(MiCapa()))
