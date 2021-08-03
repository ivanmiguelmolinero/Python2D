#-------------------------------------------------------------------------------
# Name:        ejemplo_animacion_2
# Purpose:
#
# Author:      ivijo
#
# Created:     03/08/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cocos
from pyglet.image import load, ImageGrid

class MiCapa(cocos.layer.Layer):
    is_event_handler = True
    
    def __init__(self):
        super().__init__()

    def on_mouse_press(self, x ,y, buttons, modifiers):
        mi_secuencia = ImageGrid(load('./Capitulo1/secuencia_explosion.png'), 4, 4)
        mi_animacion = mi_secuencia.get_animation(0.05, loop = False)
        self.mi_sprite = cocos.sprite.Sprite(mi_animacion, (x, y))
        self.add(self.mi_sprite)

if __name__ == '__main__':
    cocos.director.director.init(caption = 'Ejemplo animación 1')
    mi_escena = cocos.scene.Scene(MiCapa())
    cocos.director.director.run(mi_escena)