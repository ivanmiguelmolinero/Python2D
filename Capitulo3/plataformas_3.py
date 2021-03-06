#-------------------------------------------------------------------------------
# Name:        plataformas_3
# Purpose:
#
# Author:      ivijo
#
# Created:     18/08/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cocos
from pyglet import window
from pyglet.libs.win32.constants import PROCESS_CREATE_PROCESS
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
            personaje.x = 0
            Escena2()
        if personaje.pista == 2 and self.x < 0:
            personaje.x = 640
            Escena1()
        if personaje.pista == 2 and self.x > 640:
            personaje.x = 0
            Escena3()
        if personaje.pista == 3 and self.x < 0:
            personaje.x = 640
            Escena2()


class Control(Action):
    def step(self, dt):
        self.target.update(dt)


class Escena1(Scene):
    def __init__(self):
        global personaje, mapa_colision
        super().__init__()
        mi_mapa = load_tmx('mapa5.tmx')['capa0']
        if 'personaje' not in globals():
            personaje = MiGuerrero('mi_guerrero_1.png')
            personaje.position = (200, 200)
            personaje.do(Control())
        personaje.pista = 1

        manejador_scroll = ScrollingManager()
        manejador_scroll.add(mi_mapa)

        capa_personaje = ScrollableLayer()
        capa_personaje.add(personaje)

        if 'mapa_colision' not in globals():
            mapa_colision = RectMapCollider()
            mapa_colision.on_bump_handler = mapa_colision.on_bump_slide
        personaje.man_col = make_collision_handler(mapa_colision, mi_mapa)

        self.add(manejador_scroll, z = 0)
        self.add(capa_personaje, z = 1)
        director.run(self)


class Escena2(Scene):
    def __init__(self):
        super().__init__()
        personaje.pista = 2
        mi_mapa2 = load_tmx('mapa6.tmx')['capa0']

        manejador_scroll = ScrollingManager()
        manejador_scroll.add(mi_mapa2)

        capa_personaje = ScrollableLayer()
        capa_personaje.add(personaje)

        personaje.man_col = make_collision_handler(mapa_colision, mi_mapa2)

        self.add(manejador_scroll, z = 0)
        self.add(capa_personaje, z = 1)
        director.run(self)


class Escena3(Scene):
    def __init__(self):
        super().__init__()
        personaje.pista = 3
        mi_mapa3 = load_tmx('mapa7.tmx')['capa0']

        manejador_scroll = ScrollingManager()
        manejador_scroll.add(mi_mapa3)

        capa_personaje = ScrollableLayer()
        capa_personaje.add(personaje)

        personaje.man_col = make_collision_handler(mapa_colision, mi_mapa3)

        self.add(manejador_scroll, z = 0)
        self.add(capa_personaje, z = 1)
        director.run(self)


if __name__ == '__main__':
    ventana = director.init(width = 640, height = 480, caption = 'Plataformas 3')
    ventana.set_location(500, 300)
    man_tec = key.KeyStateHandler()
    director.window.push_handlers(man_tec)
    Escena1()