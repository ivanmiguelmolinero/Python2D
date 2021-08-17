#-------------------------------------------------------------------------------
# Name:        plataformas_2
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
from cocos.mapcolliders import RectMapCollider, make_collision_handler
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

        if personaje.pista == 1 and self.x > 640:
            pista_2()
        if personaje.pista == 2 and self.x < 0:
            pista_1()


class Control(Action):
    def step(self, dt):
        self.target.update(dt)


def pista_1():
    global personaje, mapa_colision
    mi_mapa = load_tmx('mapa3.tmx')['capa0']
    if 'personaje' not in globals():
        personaje = MiGuerrero('mi_guerrero_1.png')
        personaje.position = (200, 200)
        personaje.do(Control())
    else:
        personaje.x = 640
    personaje.pista = 1

    manejador_scroll = ScrollingManager()
    manejador_scroll.add(mi_mapa)

    capa_personaje = ScrollableLayer()
    capa_personaje.add(personaje)

    if 'mapa_colision' not in globals():
        mapa_colision = RectMapCollider()
        mapa_colision.on_bump_handler = mapa_colision.on_bump_slide
    personaje.man_col = make_collision_handler(mapa_colision, mi_mapa)

    mi_escena = Scene()
    mi_escena.add(manejador_scroll, z = 0)
    mi_escena.add(capa_personaje, z = 1)
    director.scene_stack.clear()
    director.run(mi_escena)


def pista_2():
    mi_mapa2 = load_tmx('mapa4.tmx')['capa0']
    personaje.x = 0
    personaje.pista = 2

    manejador_scroll2 = ScrollingManager()
    manejador_scroll2.add(mi_mapa2)

    capa_personaje2 = ScrollableLayer()
    capa_personaje2.add(personaje)

    personaje.man_col = make_collision_handler(mapa_colision, mi_mapa2)

    mi_escena2 = Scene()
    mi_escena2.add(manejador_scroll2, z = 0)
    mi_escena2.add(capa_personaje2, z = 1)
    director.run(mi_escena2)


def main():
    global man_tec

    ventana = director.init(width = 640, height = 480, caption = 'Plataformas 2')
    ventana.set_location(500, 300)

    man_tec = key.KeyStateHandler()
    director.window.push_handlers(man_tec)

    pista_1()


if __name__ == '__main__':
    main()