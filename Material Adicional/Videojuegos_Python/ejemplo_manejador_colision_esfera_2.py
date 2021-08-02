
import cocos
import cocos.collision_model as cm
import cocos.euclid as eu
from pyglet import image
from pyglet.window import key
from collections import defaultdict

class Actor(cocos.sprite.Sprite) :
    def __init__(self, imagen, x, y) :
        super().__init__(image.load(imagen))
        self.position = (x, y)
        self.cshape = cm.CircleShape(eu.Vector2(x, y), self.width/2)


class MiCapa(cocos.layer.Layer) :
    is_event_handler = True
    def __init__(self) :
        super().__init__()
        self.esfera_movil = Actor('mi_esfera.png', 320, 240)
        self.add(self.esfera_movil)
        for pos in [(100, 100), (540, 380), (540, 100), (100, 380)]:
            a = Actor('mi_esfera_2.png', pos[0] , pos[1])
            self.add(a)
        celda = self.esfera_movil.width * 1.25
        self.manejador_colision = cm.CollisionManagerGrid(0, 640, 0, 480, celda, celda)
        self.velocidad = 100.0
        self.teclas_pulsadas = defaultdict(int)
        self.schedule(self.update)

    def on_key_press(self, k, m) :
        self.teclas_pulsadas[k] = 1
    def on_key_release(self, k, m) :
        self.teclas_pulsadas[k] = 0

    def update(self, dt) :
        self.manejador_colision.clear()
        for _, node in self.children:
            self.manejador_colision.add(node)
        for other in self.manejador_colision.iter_colliding(self.esfera_movil):
            self.remove(other)

        x = self.teclas_pulsadas[key.RIGHT] - self.teclas_pulsadas[key.LEFT]
        y = self.teclas_pulsadas[key. UP] - self.teclas_pulsadas[key.DOWN]
        if x != 0 or y != 0:
            pos = self.esfera_movil.position
            nueva_x = pos[0] + self.velocidad * x * dt * 2
            nueva_y = pos[1] + self.velocidad * y * dt * 2
            self.esfera_movil.position = (nueva_x, nueva_y)
            self.esfera_movil.cshape.center = eu.Vector2(nueva_x, nueva_y)


if __name__ == '__main__':
    cocos.director.director.init(caption = 'Colisiones entre esferas')
    mi_escena = cocos.scene.Scene(MiCapa())
    cocos.director.director.run(mi_escena)

