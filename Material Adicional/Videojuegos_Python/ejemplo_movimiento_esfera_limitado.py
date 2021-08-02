
import cocos
from pyglet import image
from pyglet.window import key
from collections import defaultdict

class Actor(cocos.sprite.Sprite) :
    def __init__(self, imagen, x, y) :
        super().__init__(image.load(imagen))
        self.position = (x, y)

class MiCapa(cocos.layer.Layer) :
    is_event_handler = True
    def __init__(self) :
        super().__init__()
        self.mi_actor = Actor('mi_esfera.png', 320, 240)
        self.add(self.mi_actor)
        self.velocidad = 100.0
        self.teclas_pulsadas = defaultdict(int)
        self.schedule(self.update)

    def on_key_press(self, k, m) :
        self.teclas_pulsadas[k] = 1
    def on_key_release(self, k, m) :
        self.teclas_pulsadas[k] = 0

    def update(self, dt) :
        x = self.teclas_pulsadas[key.RIGHT] - self.teclas_pulsadas[key.LEFT]
        y = self.teclas_pulsadas[key. UP] - self.teclas_pulsadas[key.DOWN]
        if x != 0 or y != 0:
            posicion = self.mi_actor.position
            nueva_x = posicion[0] + self.velocidad * x * dt * 2
            nueva_y = posicion[1] + self.velocidad * y * dt * 2
            if self.mi_actor.width / 2 < nueva_x < 640 - self.mi_actor.width /2 and\
               self.mi_actor.height / 2 < nueva_y < 480 - self.mi_actor.height /2:
                    self.mi_actor.position = (nueva_x, nueva_y)

if __name__ == '__main__':
    cocos.director.director.init(caption='Movimiento limitado '
                                         'de esfera mediante teclado')
    mi_escena = cocos.scene.Scene(MiCapa())
    cocos.director.director.run(mi_escena)

