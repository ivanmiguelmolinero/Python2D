#-------------------------------------------------------------------------------
# Name:        ejemplo_particulas_fireworks
# Purpose:
#
# Author:      ivijo
#
# Created:     09/08/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer
from cocos.text import Label
from cocos.particle_systems import Fireworks

class P1(Layer):
    def __init__(self):
        super().__init__()
        mi_etiqueta = Label('Fuegos artificiales (Fireworks)', 
                            font_name = 'Consolas',
                            font_size = 18,
                            anchor_x = 'center', anchor_y = 'center')
        
        mi_etiqueta.position = (320, 384)
        p1 = Fireworks()
        p1.position = (900, 384)
        self.add(mi_etiqueta)
        self.add(p1)


if __name__ == '__main__':
    director.init(width = 1280, height = 768,
                    caption = 'Sistemas de partículas. Fuegos artificiales')
    director.window.set_location(300, 200)
    director.run(Scene(P1()))