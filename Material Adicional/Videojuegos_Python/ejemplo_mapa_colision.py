
from pyglet.window import key
from cocos.sprite import Sprite
from cocos.scene import Scene
from cocos.layer import ScrollableLayer, ScrollingManager
from cocos.tiles import load_tmx
from cocos.mapcolliders import RectMapCollider, make_collision_handler
from cocos.actions import Action
from cocos.director import director

class MiNave(Sprite):
    def __init__(self, image):
        super().__init__(image)

    def update(self, dt):
        vx = 200 * (man_tec[key.RIGHT] - man_tec[key.LEFT])
        vy = 200 * (man_tec[key.UP] - man_tec[key.DOWN])

        dx = vx * dt
        dy = vy * dt

        antes = self.get_rect()
        despues = antes.copy()
        despues.x += dx
        despues.y += dy

        self.man_col(antes, despues, vx, vy)
        self.position = despues.center


class Control(Action):
    def step(self, dt):
        self.target.update(dt)


if __name__ == '__main__':
    ventana = director.init(width=384, height=384,
                            caption='Mapa de colisión')
    ventana.set_location(500,300)

    man_tec = key.KeyStateHandler()
    director.window.push_handlers(man_tec)

    manejador_scroll = ScrollingManager()
    mi_mapa0 = load_tmx('mapa_base.tmx')['capa0']
    mi_mapa1 = load_tmx('mapa_base.tmx')['capa1']
    manejador_scroll.add(mi_mapa0)
    manejador_scroll.add(mi_mapa1)

    capa_personaje = ScrollableLayer()
    personaje = MiNave('mi_ovni_2.png')
    personaje.position = (200,100)
    personaje.do(Control())
    capa_personaje.add(personaje)

    mapa_colision = RectMapCollider()
    mapa_colision.on_bump_handler = mapa_colision.on_bump_slide
    personaje.man_col = make_collision_handler(mapa_colision, mi_mapa1)

    mi_escena = Scene()
    mi_escena.add(manejador_scroll, z=0)
    mi_escena.add(capa_personaje, z=1)
    director.run(mi_escena)



