#-------------------------------------------------------------------------------
# Name:        arcade_8
# Purpose:
#
# Author:      ivijo
#
# Created:     12/08/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame
from pyglet.image.animation import Animation
from pyglet.window import key
from pyglet.image import ImageGrid, load
from cocos.director import director
from cocos.layer import Layer
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.euclid import Vector2
from cocos.actions import Delay, CallFunc
from cocos.text import Label
from random import choice, randint
from collections import defaultdict
from cocos.collision_model import CollisionManagerBruteForce, AARectShape

class MiObjeto(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image)
        self.position = Vector2(x, y)
        self.cshape = AARectShape(self.position,
                                    self.width * 0.3,
                                    self.height * 0.3)

    def move(self, offset):
        self.position += offset
        self.cshape.center += offset

    def update(self, delta_t):
        pass


class MiMisil(MiObjeto):
    TECLAS_PULSADAS = defaultdict(int)

    def __init__(self, imagen, x, y):
        super().__init__(imagen, x, y)
        self.velocidad = Vector2(400, 0)
        self.esta_lanzado = False

    def update(self, delta_t):
        pulsadas = MiMisil.TECLAS_PULSADAS

        if pulsadas[key.SPACE] and self.esta_lanzado == False:
            self.image = load('./Capitulo2/mi_misil_2.png')
            sonido_misil = pygame.mixer.Sound("./Capitulo2/misil.wav")
            pygame.mixer.Sound.set_volume(sonido_misil, 0.1)
            pygame.mixer.Sound.play(sonido_misil)
            self.esta_lanzado = True
        elif self.esta_lanzado == True:
            self.move(Vector2(0, 10))
        else:
            movimiento = pulsadas[key.RIGHT] - pulsadas[key.LEFT]
            if movimiento != 0:
                delta_x = (self.velocidad * movimiento * delta_t)[0]
                if self.x <=  self.parent.ancho_ventana - self.width/2 - delta_x:
                    if self.x - self.width/2 + delta_x > abs(delta_x):
                        self.move(self.velocidad * movimiento * delta_t)
        if self.y > self.parent.alto_ventana:
            self.kill()

    def on_exit(self):
        self.do(Delay(1) + CallFunc(self.parent.crear_misil))


class MiRayo(MiObjeto):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.velocidad = Vector2(0, -400)

    def update(self, delta_t):
        self.move(self.velocidad * delta_t)
        if self.y < 0:
            self.kill


class MiAlien(MiObjeto):
    def __init__(self, img, x, y):
        super().__init__(img, x, y)
        self.velocidad = Vector2(150, 0)
        self.contador = 0
        self.dir = choice([-1, 1])

    def update(self, delta_t):
        if 50 < (self.position[0] + (self.dir * self.velocidad * delta_t)[0]) < 750:
            if self.contador < 100:
                self.move(self.dir * self.velocidad * delta_t)
                self.contador += 1
            else:
                self.contador = 0
                self.dir = choice([-1, 1])
        else:
            self.dir *= -1
        if randint(1, 1000) > 990:
            a = MiRayo('mi_rayo_1.png', self.x, self.y - 30)
            sonido_disparo = pygame.mixer.Sound("./Capitulo2/blaster.mp3")
            pygame.mixer.Sound.set_volume(sonido_disparo, 0.25)
            pygame.mixer.Sound.play(sonido_disparo)
            self.parent.add(a)


class MiEtiqueta(Label):
    def __init__(self, texto, x, y, c = (255, 255, 255, 255)):
        super().__init__(texto, (x, y), font_name = 'Consolas', font_size = 14,
                        color = c,
                        anchor_x = 'center', anchor_y = 'center')


class CapaInicio(Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()
        self.add(MiEtiqueta('Pulsa un botón del ratón para iniciar', 400, 325))
        pygame.mixer.music.load('./Capitulo2/musica_inicio.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def on_mouse_press(self, x, y, buttons, modifiers):
        a = MiHUD()
        pygame.mixer.music.stop()
        sonido_risa = pygame.mixer.Sound("./Capitulo2/risa.mp3")
        pygame.mixer.Sound.set_volume(sonido_risa, 1)
        pygame.mixer.Sound.play(sonido_risa)
        start = lambda : director.replace(Scene(MiCapa(a), a))
        self.do(Delay(5.25) + CallFunc(start))


class CapaGanador(Layer):
    def __init__(self):
        super().__init__()
        self.add(MiEtiqueta('¡Has derrotado al Imperio!', 400, 325))
        sonido_victoria = pygame.mixer.Sound("./Capitulo2/sonido_victoria.mp3")
        pygame.mixer.Sound.set_volume(sonido_victoria, 1)
        pygame.mixer.Sound.play(sonido_victoria)
        f1 = lambda : director.replace(Scene(CapaInicio()))
        self.do(Delay(10) + CallFunc(f1))


class CapaGameOver(Layer):
    def __init__(self):
        super().__init__()
        self.add(MiEtiqueta('GAME OVER', 400, 325))
        sonido_gameover = pygame.mixer.Sound("./Capitulo2/sonido_gameover.mp3")
        pygame.mixer.Sound.set_volume(sonido_gameover, 1)
        pygame.mixer.Sound.play(sonido_gameover)
        f1 = lambda : director.replace(Scene(CapaInicio()))
        self.do(Delay(10) + CallFunc(f1))



class MiCapa(Layer):
    is_event_handler = True

    def on_key_press(self, k , _):
        MiMisil.TECLAS_PULSADAS[k] = 1

    def on_key_release(self, k, _):
        MiMisil.TECLAS_PULSADAS[k] = 0
    
    def __init__(self, HUD):
        super().__init__()
        pygame.mixer.music.load('./Capitulo2/starwars8bit.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.mi_HUD = HUD
        self.ancho_ventana, self.alto_ventana = director.get_window_size()
        self.man_col = CollisionManagerBruteForce()
        self.crear_misil()
        self.crear_aliens()
        self.schedule(self.update)

    def crear_misil(self):
        self.misil = MiMisil('mi_misil.png', self.ancho_ventana * 0.5, 50)
        self.misil.TECLAS_PULSADAS[key.RIGHT] = 0
        self.misil.TECLAS_PULSADAS[key.LEFT] = 0
        self.add(self.misil)

    def crear_aliens(self):
        for i in range(6):
            alien = MiAlien('mi_ovni_1.png', self.ancho_ventana * 0.5, 600 - i*40)
            self.add(alien)

    def update(self, dt):
        sin_ovnis = True
        for data in self.children:
            if isinstance(data[1], MiAlien):
                sin_ovnis = False
        if sin_ovnis:
            pygame.mixer.music.stop()
            director.replace(Scene(CapaGanador()))

        self.man_col.clear()
        for _, node in self.children:
            if isinstance(node, MiObjeto):
                node.update(dt)
        for _, node in self.children:
            if isinstance(node, MiObjeto):
                self.man_col.add(node)
        
        self.collide(self.misil)

    def collide(self, node):
        if node is not None:
            for other in self.man_col.iter_colliding(node):
                sonido_explosion = pygame.mixer.Sound("./Capitulo2/explosion.wav")
                pygame.mixer.Sound.set_volume(sonido_explosion, 0.25)
                pygame.mixer.Sound.play(sonido_explosion)
                if self.children.count((0, other)) != 0:
                    other.kill()
                    if isinstance(other, MiAlien):
                        self.mi_HUD.puntos += 20
                        self.mi_HUD.update()
                if self.children.count((0, node)) != 0:
                    node.kill()
                    if node.y == 50:
                        self.mi_HUD.vidas -= 1
                        self.mi_HUD.update()
                seq = ImageGrid(load('./Capitulo2/secuencia_explosion.png'), 4, 4)
                anim = Animation.from_image_sequence(seq, 0.05, False)
                self.mi_sprite = Sprite(anim, (other.x, other.y))
                self.add(self.mi_sprite)
                self.do(Delay(0.8) + CallFunc(self.mi_sprite.kill))


class MiHUD(Layer):
    def __init__(self):
        super().__init__()
        self.vidas = 3
        self.puntos = 0
        self.update()

    def update(self):
        self.children = []
        texto_vidas = 'Vidas: ' + str(self.vidas)
        etiqueta_vidas = MiEtiqueta(texto_vidas, 50, 640)
        texto_puntos = 'Puntos: ' + str(self.puntos)
        etiqueta_puntos = MiEtiqueta(texto_puntos, 680, 640)
        self.add(etiqueta_vidas)
        self.add(etiqueta_puntos)
        if self.vidas == 0:
            pygame.mixer.music.stop()
            director.replace(Scene(CapaGameOver()))


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    ventana = director.init(caption = 'Protege La Tierra', width = 800, height = 650)
    ventana.set_location(500, 100)
    director.run(Scene(CapaInicio()))

