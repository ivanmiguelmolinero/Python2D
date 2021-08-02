
from pyglet.window import key
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ScrollableLayer, ScrollingManager
from cocos.sprite import Sprite
from cocos.actions import Driver

class MueveOvni(Driver):
    def __init__(self):
        super().__init__()

    def step(self, dt):
        super().step(dt)
        self.target.rotation += (teclas[key.RIGHT] - teclas[key.LEFT]) * 150 * dt
        self.target.acceleration = (teclas[key.UP] - teclas[key.DOWN]) * 400

        manejador_scroll.force_focus(self.target.x, self.target.y)


if __name__ == '__main__':

    teclas = key.KeyStateHandler()

    director.init(width = 640, height = 480, caption = 'Ejemplo scroll 1')
    director.window.set_location(300, 80)
    director.window.push_handlers(teclas)

    capa_sprite = ScrollableLayer()
    mi_ovni = Sprite('mi_ovni_2.png')
    mi_ovni.max_forward_speed = 300
    mi_ovni.max_reverse_speed = -300
    capa_sprite.add(mi_ovni)

    capa_fondo =ScrollableLayer()
    mi_fondo = Sprite('universo_original.jpg')
    mi_fondo.position = (0, 0)
    capa_fondo.add(mi_fondo)

    manejador_scroll = ScrollingManager()
    manejador_scroll.add(capa_fondo)
    manejador_scroll.add(capa_sprite)

    mi_ovni.do(MueveOvni())

    mi_escena = Scene(manejador_scroll)
    director.run(mi_escena)

