
from pyglet.window import key
from cocos.sprite import Sprite
from cocos.scene import Scene
from cocos.layer import ScrollableLayer, ScrollingManager
from cocos.tiles import load_tmx, RectMapLayer
from cocos.mapcolliders import RectMapCollider, make_collision_handler
from cocos.actions import Action
from cocos.director import director

class MiGuerrero(Sprite):
    en_suelo = True
    VEL_MOV = 200
    VEL_SALTO = 400
    GRAVEDAD = -800

    def __init__(self, image, mod_col, capa_col):
        super().__init__(image)
        self.velocidad = (0,0)
        self.mc = mod_col
        self.mc.on_bump_handler = self.mc.on_bump_slide
        self.cc = capa_col

    def update(self, dt):
        vx, vy = self.velocidad

        vx = (man_tec[key.RIGHT] - man_tec[key.LEFT]) * self.VEL_MOV
        vy += self.GRAVEDAD * dt
        if self.en_suelo and man_tec[key.SPACE]:
            vy = self.VEL_SALTO

        dx = vx * dt
        dy = vy * dt

        antes = self.get_rect()
        despues = antes.copy()
        despues.x += dx
        despues.y += dy

        self.velocidad = self.mc.collide_map(self.cc, antes, despues, vx, vy)
        self.en_suelo = (despues.y == antes.y)
        self.position = despues.center


def actualiza(dt):
    for objeto in capa_personaje.children:
        objeto[1].update(dt)


def main():
    global man_tec, mi_mapa, capa_personaje

    ventana = director.init(width=640, height=480, caption='Plataformas 1')
    ventana.set_location(500,300)

    man_tec = key.KeyStateHandler()
    director.window.push_handlers(man_tec)

    manejador_scroll = ScrollingManager()
    mi_mapa = load_tmx('mapa3.tmx')['capa0']
    manejador_scroll.add(mi_mapa)

    capa_personaje = ScrollableLayer()
    personaje = MiGuerrero('mi_guerrero_1.png', RectMapCollider(), mi_mapa)
    personaje.position = (200, 200)
    capa_personaje.add(personaje)

    mi_escena = Scene()
    mi_escena.add(manejador_scroll, z = 0)
    mi_escena.add(capa_personaje, z = 1)
    mi_escena.schedule(actualiza)
    director.run(mi_escena)


if __name__ == '__main__':
    main()

