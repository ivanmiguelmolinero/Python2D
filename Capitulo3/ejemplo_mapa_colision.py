#-------------------------------------------------------------------------------
# Name:        ejemplo_mapa_colision
# Purpose:
#
# Author:      ivijo
#
# Created:     16/08/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from cocos import director
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
        self.vy = 200
        self.vx = 200

    def update(self, dt):
        self.vx = 200 * (man_tec[key.RIGHT] - man_tec[key.LEFT])
        self.vy = 200 * (man_tec[key.UP] - man_tec[key.DOWN])

        dx = self.vx * dt
        dy = self.vy * dt

        antes = self.get_rect()
        despues = antes.copy()
        despues.x += dx
        despues.y += dy

        self.man_col(antes, despues, self.vx, self.vy)
        self.position = despues.center


class Control(Action):
    def step(self, dt):
        if self.target.vx != 0 and self.target.vy != 0:
            pass
        else:
            global personaje_frente
            global personaje_espalda
            global personaje_derecha
            global personaje_izquierda
            if self.target.vy < 0 and not personaje_frente:
                self.posicion('bruno_frente.png')
                personaje_frente = True
                personaje_espalda = False
                personaje_derecha = False
                personaje_izquierda = False

            if self.target.vy > 0 and not personaje_espalda:
                self.posicion('bruno_espalda.png')
                personaje_frente = False
                personaje_espalda = True
                personaje_derecha = False
                personaje_izquierda = False

            if self.target.vx > 0 and not personaje_derecha:
                self.posicion('bruno_derecha.png')
                personaje_frente = False
                personaje_espalda = False
                personaje_derecha = True
                personaje_izquierda = False

            if self.target.vx < 0 and not personaje_izquierda:
                self.posicion('bruno_izquierda.png')
                personaje_frente = False
                personaje_espalda = False
                personaje_derecha = False
                personaje_izquierda = True


        self.target.update(dt)
    
    def posicion(self, image):
        pos_x = self.target.x
        pos_y = self.target.y
        self.target.kill()
        personaje = MiNave(image)
        personaje.position = (pos_x, pos_y)
        personaje.do(Control())
        capa_personaje.add(personaje)
        personaje.man_col = make_collision_handler(mapa_colision, mi_mapa1)


if __name__ == '__main__':
    ventana = director.init(width = 384, height = 384,
                            caption = 'Mapa de colisión')
    ventana.set_location(500, 300)

    man_tec = key.KeyStateHandler()
    director.window.push_handlers(man_tec)

    manejador_scroll = ScrollingManager()
    mi_mapa0 = load_tmx('mapa_base.tmx')['Fondo']
    mi_mapa1 = load_tmx('mapa_base.tmx')['Obstáculos']
    manejador_scroll.add(mi_mapa0)
    manejador_scroll.add(mi_mapa1)

    capa_personaje = ScrollableLayer()
    personaje = MiNave('bruno_espalda.png')
    personaje.position = (200, 100)
    personaje.do(Control())
    personaje_espalda = True
    personaje_frente = False
    personaje_derecha = False
    personaje_izquierda = False
    capa_personaje.add(personaje)

    mapa_colision = RectMapCollider()
    mapa_colision.on_bump_handler = mapa_colision.on_bump_slide
    personaje.man_col = make_collision_handler(mapa_colision, mi_mapa1)

    mi_escena = Scene()
    mi_escena.add(manejador_scroll, z = 0)
    mi_escena.add(capa_personaje, z = 1)
    director.run(mi_escena)