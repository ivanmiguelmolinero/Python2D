
from pyglet.window import key
from pyglet.image import load, ImageGrid, Animation
from cocos.director import director
from cocos.layer import Layer
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.euclid import Vector2
from cocos.audio.effect import Effect
from cocos.collision_model import CollisionManagerBruteForce, AARectShape
from cocos.actions import Delay, CallFunc
from random import choice, randint
from collections import defaultdict

class MiObjeto(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image)
        self.position = Vector2(x, y)
        self.cshape = AARectShape(self.position,
                                  self.width * 0.5,
                                  self.height * 0.5)

    def move(self, offset):
        self.position += offset
        self.cshape.center += offset

    def update(self, delta_t):
        pass


class MiMisil(MiObjeto):
    TECLAS_PULSADAS = defaultdict(int)

    def __init__(self,imagen, x, y):
        super().__init__(imagen, x, y)
        self.velocidad = Vector2(400, 0)
        self.esta_lanzado = False

    def update(self, delta_t):
        pulsadas = MiMisil.TECLAS_PULSADAS
        if pulsadas[key.SPACE] and self.esta_lanzado == False:
            self.image = load('mi_misil_2.png')
            sonido_misil = Effect('misil.wav')
            sonido_misil.play()
            self.esta_lanzado = True
        elif self.esta_lanzado == True:
            self.move(Vector2(0,10))
        else:
            movimiento = pulsadas[key.RIGHT] - pulsadas[key.LEFT]
            if movimiento != 0:
                delta_x = (self.velocidad * movimiento * delta_t)[0]
                if self.x  <= self.parent.ancho_ventana - self.width/2 - delta_x:
                    if self.x - self.width/2 + delta_x > abs(delta_x):
                        self.move(self.velocidad * movimiento * delta_t)
        if self.y > self.parent.alto_ventana:
            self.kill()

    def on_exit(self):
        self.do(Delay(1) + CallFunc(self.parent.crear_misil))


class MiRayo(MiObjeto):
    def __init__(self,imagen, x, y):
        super().__init__(imagen, x, y)
        self.velocidad = Vector2(0, -400)

    def update(self, delta_t):
        self.move(self.velocidad * delta_t)
        if self.y < 0:
            self.kill()


class MiAlien(MiObjeto):
    def __init__(self, img, x, y):
        super().__init__(img, x, y)
        self.velocidad = Vector2(100, 0)
        self.contador = 0
        self.dir = choice([-1,1])

    def update(self, delta_t):
        if 50 < (self.position[0] + (self.dir * self.velocidad * delta_t)[0]) < 750:
            if self.contador < 100:
                self.move(self.dir * self.velocidad * delta_t)
                self.contador += 1
            else:
                self.contador = 0
                self.dir = choice([-1,1])
        else:
            self.dir *= -1
        if randint(1,1000) > 990:
            a = MiRayo('mi_rayo.png', self.x, self.y -30)
            self.parent.add(a)


class MiCapa(Layer):
    is_event_handler = True

    def on_key_press(self, k, _):
        MiMisil.TECLAS_PULSADAS[k] = 1

    def on_key_release(self, k, _):
        MiMisil.TECLAS_PULSADAS[k] = 0

    def __init__(self):
        super().__init__()
        self.ancho_ventana, self.alto_ventana = director.get_window_size()
        self.man_col = CollisionManagerBruteForce()
        self.crear_misil()
        self.crear_alien()
        self.schedule(self.update)

    def crear_misil(self):
        self.misil = MiMisil('mi_misil.png', self.ancho_ventana * 0.5, 50)
        self.add(self.misil)

    def crear_alien(self):
        self.mi_alien = MiAlien('mi_ovni_1.png', self.ancho_ventana * 0.5, 600)
        self.add(self.mi_alien)

    def update(self, dt):
        self.man_col.clear()
        for _, node in self.children:
            if isinstance(node, MiObjeto):
                node.update(dt)
        for _, node in self.children:
            if isinstance(node, MiObjeto):
                self.man_col.add(node)

        self.collide(self.misil)

    def collide(self, node):
        if node is not None:
            for other in self.man_col.iter_colliding(node):
                effect = Effect('explosion.wav')
                effect.play()
                if self.children.count((0, other)) != 0:
                    other.kill()
                if self.children.count((0, node)) != 0:
                    node.kill()
                seq = ImageGrid(load('secuencia_explosion.png'), 4, 4)
                anim = Animation.from_image_sequence(seq, 0.05, False)
                self.mi_sprite = Sprite(anim, (other.x, other.y))
                self.add(self.mi_sprite)
                self.do(Delay(0.8) + CallFunc(self.mi_sprite.kill))


if __name__ == '__main__':
    director.init(caption='Protege La Tierra',
                  width=800, height=650, audio_backend='sdl')
    mi_escena = Scene(MiCapa())
    director.run(mi_escena)
