#-------------------------------------------------------------------------------
# Name:        ejemplo_menu
# Purpose:
#
# Author:      ivijo
#
# Created:     29/07/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.menu import *

class MiMenu(Menu):
    def __init__(self):
        super().__init__("Menú principal")

        item1 = ToggleMenuItem('Sonido: ', self.eleccion_sonido, True)

        resoluciones = ['640x480', '800x600', '1024x768', '1280x720', '1600x900']
        item2 = MultipleMenuItem('Resolución: ', self.eleccion_resolucion, resoluciones)

        colores = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 200, 200)]
        item3 = ColorMenuItem('Color: ', self.eleccion_color, colores)

        item4 = EntryMenuItem('Dificultad(1-10): ', self.eleccion_dificultad,
                                '', max_length=2)
        item5 = ImageMenuItem('mi_guerrero_2.png', self.on_image_callback)
        item6 = MenuItem('Salir', self.salir)

        self.create_menu([item1, item2, item3, item4, item5, item6])

    def eleccion_sonido(self, b):
        if b:
            sel = 'activado'
        else:
            sel = 'desactivado'
        print('Tu elección de audio es: ', sel)

    def eleccion_resolucion(self, valor):
        print('Has elegido la resolución número {}'.format(valor+1))

    def eleccion_color(self, valor):
        print('Has elegido el color número {}'.format(valor+1))

    def eleccion_dificultad(self, valor):
        print('Has elegido el nivel dificultad', valor)

    def on_image_callback(self):
        print('Has elegido comenzar el juego')

    def salir(self):
        director.window.close()
        print('Has elegido salir')

def main():
    ventana = director.init(width=800, height=600, caption='')
    ventana.set_location(500,200)
    director.run(Scene(MiMenu()))

if __name__ == '__main__':
    main()