#-------------------------------------------------------------------------------
# Name:        plataformas_1_objetos
# Purpose:
#
# Author:      ivijo
#
# Created:     17/08/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from pyglet.window import key
from cocos.sprite import Sprite
from cocos.scene import Scene
from cocos.layer import ScrollableLayer, ScrollingManager
from cocos.tiles import load_tmx
from cocos.mapcolliders import TmxObjectMapCollider, make_collision_handler
from cocos.actions import Action
from cocos.director import director

class MiGuerrero(Sprite):
    en_suelo = True
    VEL_MOV = 200
    VEL_SALTO = 400
    GRAVEDAD = -800

    def __init__(self, image):
        super().__init__(image)
        self.velocidad = (0, 0)

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

        self.velocidad = self.man_col(antes, despues, vx, vy)
        self.en_suelo = (despues.y == antes.y)
        self.position = despues.center


class Control(Action):
    def step(self, dt):
        self.target.update(dt)


def main():
    global man_tec

    ventana = director.init(width = 640, height = 480, caption = 'Plataformas 1 objetos')
    ventana.set_location(500, 300)

    man_tec = key.KeyStateHandler()
    director.window.push_handlers(man_tec)

    manejador_scroll = ScrollingManager()
    mi_mapa1 = load_tmx('mapa3_2.tmx')['capa0']
    mi_mapa2 = load_tmx('mapa3_2.tmx')['capa_objetos']
    manejador_scroll.add(mi_mapa1)
    manejador_scroll.add(mi_mapa2)

    capa_personaje = ScrollableLayer()
    personaje = MiGuerrero('mi_guerrero_1.png')
    personaje.position = (200, 200)
    personaje.do(Control())
    capa_personaje.add(personaje)

    mapa_colision = TmxObjectMapCollider()
    mapa_colision.on_bump_handler = mapa_colision.on_bump_slide
    personaje.man_col = make_collision_handler(mapa_colision, mi_mapa2)

    mi_escena = Scene()
    mi_escena.add(manejador_scroll, z = 0)
    mi_escena.add(capa_personaje, z = 1)
    director.run(mi_escena)


if __name__ == '__main__':
    main()