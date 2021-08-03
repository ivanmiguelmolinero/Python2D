#-------------------------------------------------------------------------------
# Name:        ejemplo_manejador_colision_esfera
# Purpose:
#
# Author:      ivijo
#
# Created:     03/08/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cocos
import cocos.collision_model as cm
import  cocos.euclid as eu
from pyglet import image
from pyglet.window import key
from collections import defaultdict

class Actor(cocos.sprite.Sprite):
    def __init__(self, imagen, x, y):
        super().__init__(image.load(imagen))
        self.position = (x, y)
        self.cshape = cm.CircleShape(eu.Vector2(x ,y), self.width/2)


class MiCapa(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        self.esfera_movil = Actor('./Capitulo1/mi_esfera.png', 320, 240)
        self.add(self.esfera_movil)
        for pos in [(100, 100), (540, 380), (540, 100), (100, 380)]:
            a = Actor('./Capitulo1/mi_esfera2.png', pos[0], pos[1])
            self.add(a)
        self.manejador_colision = cm.CollisionManagerBruteForce()
        self.velocidad = 100.0
        self.teclas_pulsadas = defaultdict(int)
        self.schedule(self.update) 
        
    def on_key_press(self, k, m):
        self.teclas_pulsadas[k] = 1
    def on_key_release(self, k , m):
        self.teclas_pulsadas[k] = 0
    
    def update(self, dt):
        self.manejador_colision.clear()
        for _, node in self.children:
            self.manejador_colision.add(node)
        for other in self.manejador_colision.iter_colliding(self.esfera_movil):
            self.remove(other)

        x = self.teclas_pulsadas[key.RIGHT] - self.teclas_pulsadas[key.LEFT]
        y = self.teclas_pulsadas[key.UP] - self.teclas_pulsadas[key.DOWN]
        