
import cocos
from cocos.actions import *

class MisAcciones(cocos.layer.ColorLayer):

    def __init__(self):
        super().__init__(64, 200, 255, 255)

        mi_sprite = cocos.sprite.Sprite('mi_ovni_1.png')
        mi_sprite.position = 590, 240
        mi_sprite.scale = 1.5
        self.add(mi_sprite)

        mi_sprite.do(CallFuncS(lambda obj: self.discontinuo(obj, 5, (-100, 0), 1)))
        mi_sprite.do(Delay(6) + CallFuncS(lambda obj: self.mover_girando(obj, (550, 80), 3, 3)))
        mi_sprite.do(Delay(9) + AccelDeccel(MoveBy((0,350), 3) | RotateBy(360, 3)))
        mi_sprite.do(Delay(12) + Accelerate((MoveBy((-450,0), 3) | RotateBy(360, 3)), 4))
        mi_sprite.do(Delay(16) + (MoveBy((0,-400), 3) | FadeOut(3)))

    def discontinuo(self, obj, n_pasos, vector, tiempo):
        coor_x = obj.x
        coor_y = obj.y
        for i in range(1, n_pasos + 1):
            obj.do(Delay(i * tiempo) + Place((coor_x + i*vector[0], coor_y)))

    def mover_girando(self, obj, coor, n_giros, tiempo):
        obj.do(MoveTo((coor[0], coor[1]), tiempo) | RotateBy(360 * n_giros, tiempo))


if __name__ == "__main__":
    cocos.director.director.init(caption = 'Ejemplo 3 de acciones')
    mi_capa = MisAcciones()
    mi_escena = cocos.scene.Scene(mi_capa)
    cocos.director.director.run(mi_escena)


