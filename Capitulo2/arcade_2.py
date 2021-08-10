#-------------------------------------------------------------------------------
# Name:        arcade_2
# Purpose:
#
# Author:      ivijo
#
# Created:     10/08/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame
from pyglet.window import key
from pyglet.image import load
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

    def __init__(self, imagen, x, y):
        super().__init__(imagen, x, y)
        self.velocidad = Vector2(400, 0)
        self.esta_lanzado = False

    def update(self, delta_t):
        pulsadas = MiMisil.TECLAS_PULSADAS

        if pulsadas[key.SPACE] and self.esta_lanzado == False:
            self.image = load('./Capitulo2/mi_misil_2.png')
            sonido_misil = pygame.mixer.Sound("./Capitulo2/misil.wav")
            pygame.mixer.Sound.set_volume(sonido_misil, 0.25)
            pygame.mixer.Sound.play(sonido_misil)
            self.esta_lanzado = True
        elif self.esta_lanzado == True:
            self.move(Vector2(0, 10))
        else:
            movimiento = pulsadas[key.RIGHT] - pulsadas[key.LEFT]
            if movimiento != 0:
                delta_x = (self.velocidad * movimiento * delta_t)[0]
                if self.x <=  self.parent.ancho_ventana - self.width/2 - delta_x:
                    if self.x - self.width/2 + delta_x > abs(delta_x):
                        self.move(self.velocidad * movimiento * delta_t)
        if self.y > self.parent.alto_ventana:
            self.kill()

    def on_exit(self):
        self.parent.crear_misil()


class MiCapa(Layer):
    is_event_handler = True

    def on_key_press(self, k , _):
        MiMisil.TECLAS_PULSADAS[k] = 1

    def on_key_release(self, k, _):
        MiMisil.TECLAS_PULSADAS[k] = 0
    
    def __init__(self):
        super().__init__()
        self.ancho_ventana, self.alto_ventana = director.get_window_size()
        self.crear_misil()
        self.schedule(self.update)

    def crear_misil(self):
        self.misil = MiMisil('mi_misil.png', self.ancho_ventana * 0.5, 50)
        self.add(self.misil)

    def update(self, dt):
        for _, node in self.children:
            node.update(dt)

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    ventana = director.init(caption = 'Protege La Tierra', width = 800, height = 650)
    ventana.set_location(500, 200)
    mi_escena = Scene(MiCapa())
    director.run(mi_escena)

