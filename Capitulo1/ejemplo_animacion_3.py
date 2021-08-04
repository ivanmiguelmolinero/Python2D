#-------------------------------------------------------------------------------
# Name:        ejemplo_animacion_3
# Purpose:
#
# Author:      ivijo
#
# Created:     04/08/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cocos
from cocos.sprite import Sprite
from pyglet.resource import animation

class MiCapa(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        mi_sprite = Sprite(animation('gif_animado_fuego.gif'), (x, y))
        self.add(mi_sprite)
    
if __name__ == '__main__':
    cocos.director.director.init(caption = 'Ejemplo animación 3')
    mi_escena = cocos.scene.Scene(MiCapa())
    cocos.director.director.run(mi_escena)