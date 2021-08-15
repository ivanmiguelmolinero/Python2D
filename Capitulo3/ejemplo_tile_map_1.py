#-------------------------------------------------------------------------------
# Name:        ejemplo_tile_map_1
# Purpose:
#
# Author:      ivijo
#
# Created:     15/08/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from cocos.tiles import load
from cocos.layer import ScrollingManager
from cocos.director import director
from cocos.scene import Scene

if __name__ == '__main__':
    ventana = director.init(width = 384, height = 384, caption = 'Cargar tile map')
    ventana.set_location(600, 200)

    mi_mapa = load('mapa1.tmx')["capa0"]

    manejador_scroll = ScrollingManager()
    manejador_scroll.add(mi_mapa)

    director.run(Scene(manejador_scroll))