
from pyglet.window import key
from cocos.director import director
from cocos.layer import Layer
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.euclid import Vector2
from collections import defaultdict

class MiObjeto(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image)
        self.position = Vector2(x, y)

    def move(self, offset):
        self.position += offset

    def update(self, delta_t):
        pass


class MiMisil(MiObjeto):
    TECLAS_PULSADAS = defaultdict(int)

    def __init__(self,imagen, x, y):
        super().__init__(imagen, x, y)
        self.velocidad = Vector2(400, 0)

    def update(self, delta_t):
        pulsadas = MiMisil.TECLAS_PULSADAS

        movimiento = pulsadas[key.RIGHT] - pulsadas[key.LEFT]
        if movimiento != 0:
            delta_x = (self.velocidad * movimiento * delta_t)[0]
            if self.x  <= self.parent.ancho_ventana - self.width/2 - delta_x:
                if self.x - self.width/2 + delta_x > abs(delta_x):
                    self.move(self.velocidad * movimiento * delta_t)


class MiCapa(Layer):
    is_event_handler = True

    def on_key_press(self, k, _):
        MiMisil.TECLAS_PULSADAS[k] = 1

    def on_key_release(self, k, _):
        MiMisil.TECLAS_PULSADAS[k] = 0

    def __init__(self):
        super().__init__()
        self.ancho_ventana, _ = director.get_window_size()
        self.crear_misil()
        self.schedule(self.update)

    def crear_misil(self):
        self.misil = MiMisil('mi_misil.png', self.ancho_ventana * 0.5, 50)
        self.add(self.misil)

    def update(self, dt):
        for _, node in self.children:
            node.update(dt)


if __name__ == '__main__':
    ventana = director.init(caption='Protege La Tierra', width=800, height=650)
    ventana.set_location(500,200)
    mi_escena = Scene(MiCapa())
    director.run(mi_escena)

