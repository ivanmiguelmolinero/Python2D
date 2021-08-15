#-------------------------------------------------------------------------------
# Name:        ejemplo_tile_map_4
# Purpose:
#
# Author:      ivijo
#
# Created:     15/08/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from pyglet.window import key
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import ScrollableLayer, ScrollingManager
from cocos.tiles import load
from cocos.sprite import Sprite
from cocos.actions import Move


class MueveOvni(Move):
    def __init__(self):
        super().__init__()
        self.ancho_fondo = mi_fondo.px_width
        self.alto_fondo = mi_fondo.px_height
        self.x_max = self.ancho_fondo - mi_ovni.width / 2
        self.x_min = mi_ovni.width / 2
        self.y_max = self.alto_fondo - mi_ovni.height / 2
        self.y_min = mi_ovni.height / 2

    def step(self, dt):
        super().step(dt)
        if self.x_min <= self.target.x <= self.x_max and\
            self.y_min <= self.target.y <= self.y_max:
            velocity_x = 200 * (teclas[key.RIGHT] - teclas[key.LEFT])
            velocity_y = 200 * (teclas[key.UP] - teclas[key.DOWN])
        else:
            if self.target.x >= self.x_max:
                velocity_x = velocity_y = 0
                self.target.x = self.x_max
            if self.x_min >= self.target.x:
                velocity_x = velocity_y = 0
                self.target.x = self.x_min
            if self.target.y >= self.y_max:
                velocity_x = velocity_y = 0
                self.target.y = self.y_max
            if self.y_min > self.target.y:
                velocity_x = velocity_y = 0
                self.target.y = self.y_min

        self.target.velocity = (velocity_x, velocity_y)
        manejador_scroll.set_focus(self.target.x, self.target.y)



if __name__ == '__main__':
    teclas = key.KeyStateHandler()

    ventana = director.init(width = 800, height = 600,
                            caption = 'Tile map con scroll y límites')
    ventana.set_location(500, 200)
    director.window.push_handlers(teclas)

    capa_ovni = ScrollableLayer()
    mi_ovni = Sprite('mi_ovni_2.png')
    mi_ovni.position = (650, 250)
    mi_ovni.velocity = (0, 0)
    capa_ovni.add(mi_ovni)

    mi_fondo = load('mapa2.tmx')['Capa0']

    manejador_scroll = ScrollingManager()
    manejador_scroll.add(mi_fondo)
    manejador_scroll.add(capa_ovni)

    mi_ovni.do(MueveOvni())

    mi_escena = Scene(manejador_scroll)
    director.run(mi_escena)