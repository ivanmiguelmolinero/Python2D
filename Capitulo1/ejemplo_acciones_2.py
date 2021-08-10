#-------------------------------------------------------------------------------
# Name:        ejemplo_acciones_2
# Purpose:
#
# Author:      ivijoyo
#
# Created:     30/07/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cocos
from cocos.actions import *

class MisAcciones(cocos.layer.ColorLayer):

    def __init__(self):
        super().__init__(64, 200, 255, 255)

        mi_sprite = cocos.sprite.Sprite('mi_ovni_1.png')
        mi_sprite.position = 320, 240
        mi_sprite.scale = 1.5
        self.add(mi_sprite)

        mover1 = MoveBy((250, 0), 1.5)
        mover2 = MoveTo((580, 50), 2)
        mover3 = MoveBy((-250, 0), 2)
        mover4 = MoveBy((0, 250), 2)

        saltar1 = JumpTo((70,240), 100, 10, 8)
        saltar2 = JumpBy((180, 150), 50, 3, 3)

        parpadeo = Blink(12, 2)
        difuminado = FadeOut(2)
        aparicion = FadeIn(2)

        mi_sprite.do(mover1)
        mi_sprite.do(Delay(1.5) + saltar1)
        mi_sprite.do(Delay(9.5) + saltar2)
        mi_sprite.do(Delay(12.5) + (parpadeo | mover2))
        mi_sprite.do(Delay(14.5) + (difuminado | mover3))
        mi_sprite.do(Delay(16.5) + (aparicion | mover4))


if __name__ == '__main__':
    cocos.director.director.init(caption = 'Ejemplo 2 de acciones')
    mi_capa = MisAcciones()
    mi_escena = cocos.scene.Scene(mi_capa)
    cocos.director.director.run(mi_escena)