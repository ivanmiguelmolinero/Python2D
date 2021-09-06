#-------------------------------------------------------------------------------
# Name:        ejemplo_interactuar_objetos
# Purpose:
#
# Author:      ivijo
#
# Created:     06/09/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from pyglet.window import key
from pyglet.image import load
from cocos.sprite import Sprite
from cocos.scene import Scene
from cocos.layer import ScrollableLayer, ScrollingManager
from cocos.tiles import load_tmx
from cocos.mapcolliders_plus import make_collision_handler, TmxObjectMapCollider
from cocos.actions import Action, JumpBy
from cocos.particle_systems import Sun
from cocos.director import director
from cocos.collision_model import AARectShape, CollisionManagerBruteForce
from cocos.euclid import Vector2

class MiGuerrero(Sprite):
    VEL_MOV = 200
    VEL_SALTO = 500
    GRAVEDAD = -800
    en_suelo = True
    modo = 'normal'

    def __init__(self, image):
        super().__init__(image)
        self.velocidad = (0, 0)
        self.cshape = AARectShape(Vector2(0, 0), self.width/3, self.height/3)

    def update(self, dt):
        if self.modo == 'normal':
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
            self.cshape.center = Vector2(self.position[0], self.position[1])

        if self.modo == 'liana':
            if man_tec[key.SPACE] and man_tec[key.RIGHT]:
                self.do(JumpBy((185, -20), 80, 1, 1))
                self.cshape.center = Vector2(self.position[0], self.position[1])
                self.image = load('./Capitulo5/mi_guerrero_2.png')
            elif man_tec[key.SPACE] and man_tec[key.LEFT]:
                self.do(JumpBy((-195, -20), 80, 1, 1))
                self.cshape.center = Vector2(self.position[0], self.position[1])
                self.image = load('./Capitulo5/mi_guerrero_2.png')
            
        if self.modo == 'seto':
            despues_subiendo = self.position[1] + 5 * man_tec[key.UP]
            despues_bajando = self.position[1] - 5 * man_tec[key.DOWN]
            if despues_subiendo < 720 and despues_bajando > 200:
                delta_y = 5 * man_tec[key.UP] - 5 * man_tec[key.DOWN]
                self.position += Vector2(0, delta_y)
            if man_tec[key.SPACE] and man_tec[key.LEFT]:
                self.do(JumpBy((-195, -20), 80, 1, 1))
                self.cshape.center = Vector2(self.position[0], self.position[1])
                self.image = load('./Capitulo5/mi_guerrero_2.png')


class MiObjetoInteractuable(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image)
        self.position = (x, y)
        rect = self.get_rect()
        self.cshape = AARectShape(Vector2(0, 0), self.width/3, self.height/3)
        self.cshape.center = Vector2(rect.center[0], rect.center[1])

    def update(self, dt):
        pass


class Control(Action):
    def start(self):
        self.mc = CollisionManagerBruteForce()

    def step(self, dt):
        for objeto in self.target.parent.children:
            objeto[1].update(dt)
        self.mc.clear()
        for objeto in self.target.parent.children:
            self.mc.add(objeto[1])

        colisiones_personaje = set(self.mc.iter_colliding(self.target))

        if objetos_colisionables.intersection(colisiones_personaje):
            liana_agarrada = list(lianas & colisiones_personaje)
            if liana_agarrada:
                self.target.GRAVEDAD = 0
                self.target.modo = 'liana'

                self.target.position = (liana_agarrada[0].position[0] - 12,
                                        liana_agarrada[0].position[1] - 35)
                self.target.image = load('./Capitulo5/guerrero_agarrando.png')
            if seto in colisiones_personaje:
                self.target.GRAVEDAD = 0
                self.target.modo = 'seto'
                self.target.image = load('./Capitulo5/guerrero_agarrando.png')
                self.target.position = (seto.position[0] - 35,
                                        self.target.position[1])
        else:
            self.target.modo = 'normal'
            self.target.GRAVEDAD = -800


class Escena(Scene):
    def __init__(self):
        global personaje, mapa_colision, man_tec,\
            objetos_colisionables, lianas, seto
        super().__init__()

        mi_mapa1 = load_tmx('mapa_plataformas_3.tmx')['objetos']
        mi_mapa1_1 = load_tmx('mapa_plataformas_3.tmx')['capa0']

        personaje = MiGuerrero('mi_guerrero_2.png')
        personaje.position = (200, 300)
        personaje.do(Control())

        fondo = Sprite('mi_fondo_2.png')
        fondo.position = (640, 384)

        sol = Sun()
        sol.position = (800, 650)

        liana_1 = MiObjetoInteractuable('liana.png', 440, 404)
        liana_2 = MiObjetoInteractuable('liana.png', 640, 404)
        seto = MiObjetoInteractuable('seto.png', 1260, 520)

        objetos_colisionables = {liana_1, liana_2, seto}
        lianas = {liana_1, liana_2}

        capa_fondo = ScrollableLayer()
        capa_fondo.add(fondo)
        capa_fondo.add(sol)

        manejador_scroll = ScrollingManager()
        manejador_scroll.add(mi_mapa1)
        manejador_scroll.add(mi_mapa1_1)

        capa_personaje = ScrollableLayer()
        capa_personaje.add(personaje)
        capa_personaje.add(liana_1)
        capa_personaje.add(liana_2)
        capa_personaje.add(seto)

        mapa_colision = TmxObjectMapCollider()
        mapa_colision.on_bump_handler = mapa_colision.on_bump_slide
        personaje.man_col = make_collision_handler(mapa_colision, mi_mapa1)

        self.add(capa_fondo, z = 0)
        self.add(manejador_scroll, z = 1)
        self.add(capa_personaje, z = 2)
        director.run(self)


if __name__ == '__main__':
    ventana = director.init(width = 1280, height = 768,
                            caption = 'Interactuando con objetos')
    ventana.set_location(200, 40)
    man_tec = key.KeyStateHandler()
    director.window.push_handlers(man_tec)
    Escena()