
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.actions import MoveBy, RotateBy, JumpBy, Delay

class MisAcciones(Layer):

    def __init__(self):
        super().__init__()

        mi_sprite = Sprite('mi_coche.png')
        mi_rotonda = Sprite('mi_rotonda.png')
        mi_sprite.position = 0, 320
        mi_rotonda.position = 480, 384

        self.add(mi_rotonda)
        self.add(mi_sprite)

        mover1 = MoveBy((60, 0), 1)
        mover2 = MoveBy((120, -100), 2)
        mover3 = MoveBy((100, 45), 1)
        mover4 = MoveBy((100, 0), 1)

        rotar1 = RotateBy(60, 2)
        rotar2 = RotateBy(-120, 5)
        rotar3 = RotateBy(60, 1)

        saltar1 = JumpBy((640,35), -170, 1, 5)

        paso1 = mover1
        paso2 = mover2 |rotar1
        paso3 = saltar1 | rotar2
        paso4 = mover3 | rotar3
        paso5 = mover4

        mi_sprite.do(paso1 + Delay(2) + paso2 + paso3 +  paso4 + paso5 )


if __name__ == "__main__":
    ventana = director.init(width=960, height=768, caption = 'Rotonda')
    ventana.set_location(450,100)
    mi_capa = MisAcciones()
    mi_escena = Scene(mi_capa)
    director.run(mi_escena)
