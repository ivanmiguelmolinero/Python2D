
from pyglet.window import key
from cocos.sprite import Sprite
from cocos.scene import Scene
from cocos.layer import ScrollableLayer, ScrollingManager
from cocos.tiles import load_tmx
from cocos.mapcolliders_plus import TmxObjectMapCollider, make_collision_handler
from cocos.collision_model import CircleShape
from cocos.actions import Action, Delay, CallFunc, MoveBy, Repeat
from cocos.director import director
from cocos.euclid import Vector2
from random import randint

class MiGuerrero(Sprite):
    en_suelo = True
    VEL_MOV = 200
    VEL_SALTO = 500
    GRAVEDAD = -800

    def __init__(self, image):
        super().__init__(image)
        self.velocidad = (0,0)
        self.direccion = 'derecha'
        self.hay_disparo = False

    def update(self, dt):
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
                self.disparo = MiCuchillo('mi_cuchillo_1.png', 'd',
                                          self.position[0], self.position[1])
                self.parent.add(self.disparo)
            elif self.direccion == 'izquierda':
                self.disparo = MiCuchillo('mi_cuchillo_2.png', 'i',
                                          self.position[0], self.position[1])
                self.parent.add(self.disparo)
            self.do(Delay(0.2)+ CallFunc(self.nuevo_disparo))

        dx = vx * dt
        dy = vy * dt

        antes = self.get_rect()
        despues = antes.copy()
        despues.x += dx
        despues.y += dy

        self.velocidad = self.man_col(antes, despues, vx, vy)
        self.en_suelo = (despues.y == antes.y)
        self.position = despues.center

        manejador_scroll.set_focus(despues.x, 384)

    def nuevo_disparo(self):
        self.hay_disparo = False


class MiCuchillo(Sprite):
    def __init__(self, image, dir, x, y):
        super().__init__(image)
        self.position = (x,y)
        self.direccion = dir
    def update(self, dt):
        if self.direccion == 'd':
            self.position += Vector2(20,0)
        elif self.direccion == 'i':
            self.position -= Vector2(20,0)


class MiDragon(Sprite):
    def __init__(self, image):
        super().__init__(image)
    def update(self, dt):
        if randint(1,1000) > 980:
            llama = MiFuegoDragon('mi_fuego_dragon.png', self.x -50, self.y + 40)
            self.parent.add(llama)


class MiFuegoDragon(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image)
        self.position = (x,y)

    def update(self, dt):
        self.position += Vector2(-10,0)


class Control(Action):
    def step(self, dt):
        for objeto in self.target.parent.children:
            objeto[1].update(dt)


class Escena(Scene):
    def __init__(self):
        global manejador_scroll
        super().__init__()
        mi_mapa1 = load_tmx('mapa_plataformas.tmx')['objetos']
        mi_mapa1_1 = load_tmx('mapa_plataformas.tmx')['capa0']

        dragon = MiDragon('mi_dragon.png')
        dragon.position = (2500,300)

        personaje = MiGuerrero('mi_guerrero_2.png')
        personaje.position = (200,300)

        dragon.do(Repeat(MoveBy((0,300), 1) + MoveBy((0,-300), 1)))
        personaje.do(Control())

        capa_fondo = ScrollableLayer()
        for i in range(4):
            a =Sprite('mi_fondo.png')
            a.position = (640 + 1280*i, 440)
            capa_fondo.add(a)

        capa_personaje = ScrollableLayer()
        capa_personaje.add(personaje)
        capa_personaje.add(dragon)

        manejador_scroll = ScrollingManager()
        manejador_scroll.add(mi_mapa1, z=0)
        manejador_scroll.add(capa_fondo, z=1)
        manejador_scroll.add(mi_mapa1_1, z=2)
        manejador_scroll.add(capa_personaje, z=3)

        mapa_colision = TmxObjectMapCollider()
        mapa_colision.on_bump_handler = mapa_colision.on_bump_slide
        personaje.man_col = make_collision_handler(mapa_colision, mi_mapa1)

        self.add(manejador_scroll)
        director.run(self)


if __name__ == '__main__':
    ventana = director.init(width=1280, height=768, caption='Guerrero vs Dragón')
    ventana.set_location(300,200)
    man_tec = key.KeyStateHandler()
    director.window.push_handlers(man_tec)
    Escena()
