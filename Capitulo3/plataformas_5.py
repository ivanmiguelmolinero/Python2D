#-------------------------------------------------------------------------------
# Name:        plataformas_5
# Purpose:
#
# Author:      ivijo
#
# Created:     19/08/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from pyglet.window import key
from cocos.sprite import Sprite
from cocos.scene import Scene
from cocos.layer import ScrollableLayer, ScrollingManager
from cocos.tiles import load_tmx
from cocos.mapcolliders_plus import TmxObjectMapCollider, make_collision_handler
from cocos.actions import Action
from cocos.director import director

class MiGuerrero(Sprite):
    en_suelo = True
    VEL_MOV = 200
    VEL_SALTO = 500
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
        
        dx = vx *dt
        dy = vy * dt

        antes = self.get_rect()
        despues = antes.copy()
        despues.x += dx
        despues.y += dy

        self.velocidad = self.man_col(antes, despues, vx, vy)
        self.en_suelo = (despues.y == antes.y)
        self.position = despues.center

        manejador_scroll.set_focus(despues.x, 384)


class Control(Action):
    def step(self, dt):
        self.target.update(dt)


class Escena(Scene):
    def __init__(self):
        global manejador_scroll
        super().__init__()
        mi_mapa1 = load_tmx('mapa11.tmx')['objetos']
        mi_mapa1_1 = load_tmx('mapa11.tmx')['capa0']

        personaje = MiGuerrero('mi_guerrero_2.png')
        personaje.position = (200, 300)
        personaje.do(Control())

        capa_personaje = ScrollableLayer()
        capa_personaje.add(personaje)

        manejador_scroll = ScrollingManager()
        manejador_scroll.add(mi_mapa1, z = 0)
        manejador_scroll.add(mi_mapa1_1, z = 1)
        manejador_scroll.add(capa_personaje, z = 2)

        mapa_colision = TmxObjectMapCollider()
        mapa_colision.on_bump_handler = mapa_colision.on_bump_slide
        personaje.man_col = make_collision_handler(mapa_colision, mi_mapa1)

        self.add(manejador_scroll)
        director.run(self)


if __name__ == '__main__':
    ventana = director.init(width = 1280, height = 768, caption = 'Plataformas 5')
    ventana.set_location(200, 40)
    man_tec = key.KeyStateHandler()
    director.window.push_handlers(man_tec)
    Escena()