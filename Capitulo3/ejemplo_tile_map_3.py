#-------------------------------------------------------------------------------
# Name:        ejemplo_tile_map_3
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

    def step(self, dt):
        super().step(dt)
        velocity_x = 200 * (teclas[key.RIGHT] - teclas[key.LEFT])
        velocity_y = 200 * (teclas[key.UP] - teclas[key.DOWN])
        self.target.velocity = (velocity_x, velocity_y)

        manejador_scroll.set_focus(self.target.x, self.target.y)


if __name__ == '__main__':
    teclas = key.KeyStateHandler()

    ventana = director.init(width = 800, height = 600,
                            caption = 'Tile map con scroll sin límites')
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