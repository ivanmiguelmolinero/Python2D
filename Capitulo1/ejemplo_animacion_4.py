#-------------------------------------------------------------------------------
# Name:        ejemplo_animacion_4
# Purpose:
#
# Author:      ivijo
#
# Created:     04/08/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cocos
from cocos.actions import CallFunc, Delay
from cocos.sprite import Sprite
from pyglet.resource import animation

class MiCapa(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        mi_animacion = animation('gif_animado_explosion.gif')
        mi_sprite = Sprite(mi_animacion, (x, y))
        self.add(mi_sprite)
        tiempo_animacion = mi_animacion.get_duration()
        self.do(Delay(tiempo_animacion) + CallFunc(self.elimina_sprite))
    
    def elimina_sprite(self):
        if self.children:
            self.children[0][1].kill()
    
if __name__ == '__main__':
    cocos.director.director.init(caption = 'Ejemplo animacion 4')
    mi_escena = cocos.scene.Scene(MiCapa())
    cocos.director.director.run(mi_escena)