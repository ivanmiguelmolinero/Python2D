#-------------------------------------------------------------------------------
# Name:        juego_6
# Purpose:
#
# Author:      ivijo
#
# Created:     01/09/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame
from pygame.mixer import Sound, music
from pyglet.window import key
from cocos.sprite import Sprite
from cocos.scene import Scene
from cocos.layer import Layer, ScrollableLayer, ScrollingManager
from cocos.tiles import load_tmx
from cocos.mapcolliders_plus import TmxObjectMapCollider, make_collision_handler
from cocos.collision_model import AARectShape, CollisionManagerBruteForce, Cshape
from cocos.particle_systems import Explosion, Smoke, Sun
from cocos.particle import Color
from cocos.actions import Action, Delay, CallFunc, MoveBy, Repeat, FadeOut
from cocos.director import director
from cocos.euclid import Vector2
from cocos.text import Label
from random import randint

class MiGuerrero(Sprite):
    en_suelo = True
    VEL_MOV = 200
    VEL_SALTO = 500
    GRAVEDAD = -800

    def __init__(self, image, x, y):
        super().__init__(image)
        self.position = (x, y)
        self.velocidad = (0, 0)
        self.direccion = 'derecha'
        self.hay_disparo = False
        self.reviviendo = False
        self.cshape = AARectShape(self.position, self.width/2, self.height/2)

    def update(self, dt):
        if self.reviviendo == False:
            vx, vy = self.velocidad
            vx = (man_tec[key.RIGHT] - man_tec[key.LEFT]) * self.VEL_MOV
            vy += self.GRAVEDAD * dt
            if self.en_suelo and man_tec[key.SPACE]:
                vy = self.VEL_SALTO
            if man_tec[key.LEFT]:
                self.direccion = 'izquierda'
            if man_tec[key.RIGHT]:
                self.direccion = 'derecha'

            if man_tec[key.ENTER] and not self.hay_disparo:
                self.hay_disparo = True
                if self.direccion == 'derecha':
                    sonido_cuchillo = pygame.mixer.Sound("./Capítulo4/cuchillo.wav")
                    pygame.mixer.Sound.set_volume(sonido_cuchillo, 0.25)
                    pygame.mixer.Sound.play(sonido_cuchillo)
                    self.disparo = MiCuchillo('mi_cuchillo_1.png', 'd',
                                                self.position[0], self.position[1])
                    self.parent.add(self.disparo)
                elif self.direccion == 'izquierda':
                    sonido_cuchillo = pygame.mixer.Sound("./Capítulo4/cuchillo.wav")
                    pygame.mixer.Sound.set_volume(sonido_cuchillo, 0.25)
                    pygame.mixer.Sound.play(sonido_cuchillo)
                    self.disparo = MiCuchillo('mi_cuchillo_2.png', 'i',
                                                self.position[0], self.position[1])
                    self.parent.add(self.disparo)
                self.do(Delay(0.2) + CallFunc(self.nuevo_disparo))
            
            dx = vx *dt
            dy = vy * dt

            antes = self.get_rect()
            despues = antes.copy()
            despues.x += dx
            despues.y += dy

            self.velocidad = self.man_col(antes, despues, vx, vy)
            self.en_suelo = (despues.y == antes.y)

            if despues.x < ref_salida.x - self.width:
                self.position = despues.center
            else:
                music.stop()
                director.replace(Scene(CapaGanador()))
            self.cshape.center = Vector2(self.position[0], self.position[1])

            if despues.x >= 640:
                manejador_scroll.set_focus(despues.x, 384)

    def nuevo_disparo(self):
        self.hay_disparo = False


class MiCuchillo(Sprite):
    def __init__(self, image, dir, x, y):
        super().__init__(image)
        self.position = (x, y)
        self.direccion = dir
        self.cshape = AARectShape(self.position, self.width/5, self.height/5)

    def update(self, dt):
        coor_cuchillo = manejador_scroll.world_to_screen(self.x, self.y)[0]
        if coor_cuchillo > 1280 or coor_cuchillo < 0:
            self.kill()
        if self.direccion == 'd':
            self.position += Vector2(20, 0)
        if self.direccion == 'i':
            self.position -= Vector2(20, 0)
        self.cshape.center = Vector2(self.position[0], self.position[1])


class MiObjeto(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image)
        self.position = (x, y)

    
class MiEnemigo(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image)
        self.position = (x, y)
        self.cshape = AARectShape(self.position, self.width/2, self.height/2)

    def update(self, dt):
        self.cshape.center = Vector2(self.position[0], self.position[1])


class MiDragon(MiEnemigo):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.cshape = AARectShape(self.position, self.width/2, self.height/2)

    def update(self, dt):
        if randint(1, 1000) > 980:
            sonido_llama = Sound('./Capítulo4/fuego_dragon.wav')
            Sound.set_volume(sonido_llama, 0.05)
            Sound.play(sonido_llama)
            llama = MiFuegoDragon('mi_fuego_dragon.png', self.x - 50, self.y + 40)
            self.parent.add(llama)
        self.cshape.center = Vector2(self.position[0], self.position[1])


class MiFuegoDragon(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image)
        self.position = (x, y)
        self.cshape = AARectShape(self.position, self.width/5, self.height/5)

    def update(self, dt):
        self.position += Vector2(-10, 0)
        if self.x < 0:
            self.kill()
        self.cshape.center = Vector2(self.position[0], self.position[1])


class MiExplosion1(Explosion):
    def __init__(self, pos):
        super().__init__()
        self.position = pos
        self.auto_remove_on_finish = True
        self.total_particles = 700
        self.emission_rate = 700
        self.size = 2
        self.life = 1
        self.scale = 2
        self.start_color = Color(255, 255, 0, 255)

    def update(self, dt):
        pass


class MiExplosion2(Explosion):
    def __init__(self, pos):
        super().__init__()
        self.position = pos
        self.auto_remove_on_finish = True
        self.total_particles = 700
        self.emission_rate = 1200
        self.size = 10
        self.life = 3
        self.start_color = Color(0, 255, 100, 255)

    def update(self, dt):
        pass


class MiExplosion3(Explosion):
    def __init__(self, pos):
        super().__init__()
        self.position = pos
        self.total_particles = 100
        self.size = 2
        self.life = 1
        self.auto_remove_on_finish = True
        self.start_color = Color(0, 0, 255, 255)

    def update(self, dt):
        pass


class Control(Action):
    def start(self):
        self.rel = [set([MiGuerrero, MiFuegoDragon]), set([MiGuerrero, MiDragon]),
                    set([MiGuerrero, MiEnemigo])]
        self.mc = CollisionManagerBruteForce()

    def step(self, dt):
        self.mc.clear()
        for objeto in self.target.parent.children:
            if isinstance(objeto[1], (MiGuerrero, MiCuchillo,
                                      MiEnemigo, MiDragon, MiFuegoDragon)):
                self.mc.add(objeto[1])

        for elemento in list(self.mc.iter_all_collisions()):
            a = set([type(elemento[0]), type(elemento[1])])
            b = set([MiCuchillo, MiFuegoDragon])
            c = set([MiCuchillo, MiDragon])
            d = set([MiCuchillo, MiEnemigo])

            if a in self.rel and personaje.reviviendo == False:
                sonido = Sound('./Capítulo4/golpeo_personaje.wav')
                Sound.play(sonido)
                personaje.visible = False
                personaje.reviviendo = True
                personaje.do(Delay(1.5) + CallFunc(self.f1))
            if a == b:
                sonido = Sound('./Capítulo4/col_cuchillo_enemigo.wav')
                Sound.set_volume(sonido, 0.25)
                Sound.play(sonido)
                self.target.parent.add(MiExplosion1(elemento[0].position))
                if (0, elemento[0]) in self.target.parent.children:
                    elemento[0].kill()
                if (0, elemento[1]) in self.target.parent.children:
                    elemento[1].kill()
                hud.puntos += 5
            if a == c:
                sonido = Sound('./Capítulo4/col_cuchillo_dragon.wav')
                Sound.set_volume(sonido, 0.25)
                Sound.play(sonido)
                self.target.parent.add(MiExplosion2(elemento[0].position))
                if (0, elemento[0]) in self.target.parent.children:
                    elemento[0].kill()
                if (0, elemento[1]) in self.target.parent.children:
                    elemento[1].kill()
                hud.puntos += 50
            if a == d:
                sonido = Sound('./Capítulo4/col_cuchillo_enemigo.wav')
                Sound.set_volume(sonido, 0.25)
                Sound.play(sonido)
                self.target.parent.add(MiExplosion3(elemento[0].position))
                if (0, elemento[0]) in self.target.parent.children:
                    elemento[0].kill()
                if (0, elemento[1]) in self.target.parent.children:
                    elemento[1].kill()
                hud.puntos += 15

        for objeto in self.target.parent.children:
            if not isinstance(objeto[1], (MiObjeto, Smoke, Sun)):
                objeto[1].update(dt)

    def f1(self):
        hud.vidas -= 1
        personaje.reviviendo = False
        if hud.vidas > 0:
            personaje.visible = True


class MiEtiqueta(Label):
    def __init__(self, texto, x, y, c = (255, 255, 255, 255)):
        super().__init__(texto, (x, y), font_name = 'Consolas', font_size = 14,
                         color = c, anchor_x = 'center', anchor_y = 'center')


class MiHUD(Layer):
    def __init__(self):
        super().__init__()
        self.vidas = 2
        self.puntos = 0

    def update(self, dt):
        self.children = []
        texto_vidas = 'Vidas: ' + str(self.vidas)
        etiqueta_vidas = MiEtiqueta(texto_vidas, 70, 740, (0, 255, 0, 255))
        texto_puntos = 'Puntos: ' + str(self.puntos)
        etiqueta_puntos = MiEtiqueta(texto_puntos, 1180, 740, (0, 255, 255, 255))
        self.add(etiqueta_vidas)
        self.add(etiqueta_puntos)
        delta_scroll = manejador_scroll.world_to_screen(70, 740)[0]
        if self.vidas == 0:
            music.stop()
            director.replace(Scene(CapaGameOver()))
        self.x = 70 - delta_scroll


class CapaInicio(Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        self.add(MiEtiqueta('Pulse un botón del ratón para iniciar', 640, 384))

    def on_mouse_press(self, x, y, buttons, modifiers):
        director.replace(Escena())


class CapaGameOver(Layer):
    def __init__(self):
        super().__init__()
        self.add(MiEtiqueta('GAME OVER', 640, 384))
        self.do(Delay(3) + CallFunc(lambda : director.replace(Scene(CapaInicio()))))


class CapaGanador(Layer):
    def __init__(self):
        super().__init__()
        self.add(MiEtiqueta('¡Enhorabuena, has completado la misión!', 640, 384))
        self.do(Delay(3) + CallFunc(lambda : director.replace(Scene(CapaInicio()))))


class Escena(Scene):
    def __init__(self):
        global personaje, manejador_scroll, hud, ref_salida
        super().__init__()

        music.load('./Capítulo4/musica_fondo_retro.wav')
        music.set_volume(0.03)
        music.play(-1)

        mi_mapa1 = load_tmx('mapa_plataformas_2.tmx')['objetos']
        mi_mapa1_1 = load_tmx('mapa_plataformas_2.tmx')['capa0']

        ref_dra = mi_mapa1.find_cells(p_dragon=True)[0]
        dragon = MiDragon('mi_dragon.png', ref_dra.x, ref_dra.y)
        mi_mapa1.objects.remove(ref_dra)
        dragon.do(Repeat(MoveBy((0, 400), 1) + MoveBy((0, -400), 1)))

        ref_ara = mi_mapa1.find_cells(p_arana=True)[0]
        araña1 = MiEnemigo('mi_araña_2.png', ref_ara.x, ref_ara.y + 10)
        mi_mapa1.objects.remove(ref_ara)
        araña1.do(Repeat(MoveBy((450, 0), 3) + MoveBy((-450, 0), 3)))

        ref_ara = mi_mapa1.find_cells(p_arana_2=True)[0]
        araña2 = MiEnemigo('mi_araña_2.png', ref_ara.x, ref_ara.y + 10)
        mi_mapa1.objects.remove(ref_ara)
        araña2.do(Repeat(MoveBy((-450, 0), 3) + MoveBy((450, 0), 3)))

        ref_pila = mi_mapa1.find_cells(p_pila=True)[0]
        pila = MiObjeto('mi_pila.png', ref_pila.center[0], ref_pila.center[1])

        humo_pila = Smoke()
        humo_pila.position = pila.position + Vector2(0, 40)

        sol = Sun()
        ref_sol = mi_mapa1.find_cells(p_sol=True)[0]
        sol.position = Vector2(ref_sol.x, ref_sol.y)
        mi_mapa1.objects.remove(ref_sol)

        ref_per = mi_mapa1.find_cells(p_personaje=True)[0]
        personaje = MiGuerrero('mi_guerrero_2.png', ref_per.x, ref_per.y)
        mi_mapa1.objects.remove(ref_per)
        personaje.do(Control())

        ref_salida = mi_mapa1.find_cells(p_salida= True)[0]

        capa_fondo = ScrollableLayer()
        for i in range(4):
            a = Sprite('mi_fondo.png')
            a.position = (640 + 1280*i, 440)
            capa_fondo.add(a)

        hud = MiHUD()

        capa_personaje = ScrollableLayer()
        capa_personaje.add(dragon)
        capa_personaje.add(araña1)
        capa_personaje.add(araña2)
        capa_personaje.add(pila)
        capa_personaje.add(humo_pila)
        capa_personaje.add(sol)
        capa_personaje.add(personaje)
        capa_personaje.add(hud)

        manejador_scroll = ScrollingManager()
        manejador_scroll.add(mi_mapa1, z = 0)
        manejador_scroll.add(capa_fondo, z = 1)
        manejador_scroll.add(mi_mapa1_1, z = 2)
        manejador_scroll.add(capa_personaje, z = 3)

        mapa_colision = TmxObjectMapCollider()
        mapa_colision.on_bump_handler = mapa_colision.on_bump_slide
        personaje.man_col = make_collision_handler(mapa_colision, mi_mapa1)

        self.add(manejador_scroll)
        director.run(self)

def cierra_ventana():
    music.stop()
    director.window.close()


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    ventana = director.init(width = 1280, height = 768, caption = 'Plataformas 5')
    ventana.set_location(200, 40)
    man_tec = key.KeyStateHandler()
    director.window.push_handlers(man_tec)
    director.window.on_close = cierra_ventana
    director.run(Scene(CapaInicio()))