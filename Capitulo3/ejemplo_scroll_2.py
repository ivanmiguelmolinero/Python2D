#-------------------------------------------------------------------------------
# Name:        ejemplo_scroll_2
# Purpose:
#
# Author:      ivijo
#
# Created:     14/08/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from pyglet.window import key
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ScrollableLayer, ScrollingManager
from cocos.sprite import Sprite
from cocos.actions import Driver

class MueveOvni(Driver):
    def __init__(self):
        super().__init__()
        self.ancho_fondo = mi_fondo.width
        self.alto_fondo = mi_fondo.height
        self.x_max = self.ancho_fondo - mi_ovni.height / 2
        self.x_min = mi_ovni.height / 2
        self.y_max = self.alto_fondo - mi_ovni.height / 2
        self.y_min = mi_ovni.height / 2

    def step(self, dt):
        super().step(dt)
        self.target.rotation += (teclas[key.RIGHT] - teclas[key.LEFT]) * 150 * dt
        self.target.acceleration = (teclas[key.UP] - teclas[key.DOWN]) * 400

        manejador_scroll.set_focus(self.target.x, self.target.y, force = True)

        if self.target.x > self.x_max:
            self.target.speed = 0
            self.target.x = self.x_max
        if self.target.x < self.x_min:
            self.target.speed = 0
            self.target.x = self.x_min
        if self.target.y < self.y_min:
            self.target.speed = 0
            self.target.y = self.y_min
        if self.target.y > self.y_max:
            self.target.speed = 0
            self.target.y = self.y_max


if __name__ == '__main__':

    teclas = key.KeyStateHandler()

    director.init(width = 640, height = 480, caption = 'Ejemplo scroll 2')
    director.window.set_location(300, 80)
    director.window.push_handlers(teclas)

    capa_sprite = ScrollableLayer()
    mi_ovni = Sprite('mi_ovni_2.png')
    mi_ovni.position = (640, 436)
    mi_ovni.max_forward_speed = 300
    mi_ovni.max_reverse_speed = -300
    capa_sprite.add(mi_ovni)

    capa_fondo = ScrollableLayer()
    capa_fondo.px_width = 1280
    capa_fondo.px_height = 873
    mi_fondo = Sprite('universo_original.jpg')
    mi_fondo.position = (640, 436)
    capa_fondo.add(mi_fondo)

    manejador_scroll = ScrollingManager()
    manejador_scroll.add(capa_fondo)
    manejador_scroll.add(capa_sprite)

    mi_ovni.do(MueveOvni())

    mi_escena = Scene(manejador_scroll)
    director.run(mi_escena)