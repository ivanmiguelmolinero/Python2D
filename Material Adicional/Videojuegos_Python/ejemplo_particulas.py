

from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer
from cocos.text import Label
from cocos.particle_systems import *

class P1(Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        mi_etiqueta = Label('Fuegos artificiales (Fireworks)',
                                       font_name = 'Consolas',
                                       font_size = 18,
                                       anchor_x = 'center', anchor_y = 'center')

        mi_etiqueta.position = (320, 384)
        p1 = Fireworks()
        p1.position = (900, 384)
        self.add(mi_etiqueta)
        self.add(p1)

    def on_mouse_release(self, x, y, buttons, modifiers):
        director.replace(Scene(P2()))


class P2(Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        mi_etiqueta = Label('Explosión (Explosion)',
                                       font_name = 'Consolas',
                                       font_size = 18,
                                       anchor_x = 'center', anchor_y = 'center')

        mi_etiqueta.position = (320, 384)
        p2 = Explosion()
        p2.position = (900, 440)
        self.add(mi_etiqueta)
        self.add(p2)

    def on_mouse_release(self, x, y, buttons, modifiers):
        director.replace(Scene(P3()))


class P3(Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        mi_etiqueta = Label('Fuego (Fire)',
                                       font_name = 'Consolas',
                                       font_size = 18,
                                       anchor_x = 'center', anchor_y = 'center')

        mi_etiqueta.position = (320, 384)
        p3 = Fire()
        p3.position = (900, 384)
        self.add(mi_etiqueta)
        self.add(p3)

    def on_mouse_release(self, x, y, buttons, modifiers):
        director.replace(Scene(P4()))


class P4(Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        mi_etiqueta = Label('Flor (Flower)',
                                       font_name = 'Consolas',
                                       font_size = 18,
                                       anchor_x = 'center', anchor_y = 'center')

        mi_etiqueta.position = (320, 384)
        p4 = Flower()
        p4.position = (900, 384)
        self.add(mi_etiqueta)
        self.add(p4)

    def on_mouse_release(self, x, y, buttons, modifiers):
        director.replace(Scene(P5()))


class P5(Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        mi_etiqueta = Label('Sol (Sun)',
                                       font_name = 'Consolas',
                                       font_size = 18,
                                       anchor_x = 'center', anchor_y = 'center')

        mi_etiqueta.position = (320, 384)
        p5 = Sun()
        p5.position = (900, 384)
        self.add(mi_etiqueta)
        self.add(p5)

    def on_mouse_release(self, x, y, buttons, modifiers):
        director.replace(Scene(P6()))


class P6(Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        mi_etiqueta = Label('Espiral (Spiral)',
                                       font_name = 'Consolas',
                                       font_size = 18,
                                       anchor_x = 'center', anchor_y = 'center')

        mi_etiqueta.position = (320, 384)
        p6 = Spiral()
        p6.position = (900,384)
        self.add(mi_etiqueta)
        self.add(p6)

    def on_mouse_release(self, x, y, buttons, modifiers):
        director.replace(Scene(P7()))


class P7(Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        mi_etiqueta = Label('Meteorito (Meteor)',
                                       font_name = 'Consolas',
                                       font_size = 18,
                                       anchor_x = 'center', anchor_y = 'center')

        mi_etiqueta.position = (320, 384)
        p7 = Meteor()
        p7.position = (900, 384)
        self.add(mi_etiqueta)
        self.add(p7)

    def on_mouse_release(self, x, y, buttons, modifiers):
        director.replace(Scene(P8()))


class P8(Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        mi_etiqueta = Label('Galaxia (Galaxy)',
                                       font_name = 'Consolas',
                                       font_size = 18,
                                       anchor_x = 'center', anchor_y = 'center')

        mi_etiqueta.position = (320, 384)
        p8 = Galaxy()
        p8.position = (900, 384)
        self.add(mi_etiqueta)
        self.add(p8)

    def on_mouse_release(self, x, y, buttons, modifiers):
        director.replace(Scene(P9()))


class P9(Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        mi_etiqueta = Label('Humo (Smoke)',
                                       font_name = 'Consolas',
                                       font_size = 18,
                                       anchor_x = 'center', anchor_y = 'center')

        mi_etiqueta.position = (320, 384)
        p9 = Smoke()
        p9.position = (900, 384)
        self.add(mi_etiqueta)
        self.add(p9)

    def on_mouse_release(self, x, y, buttons, modifiers):
        director.replace(Scene(P1()))


if __name__ == "__main__":
    director.init(width = 1280, height = 768, caption = 'Sistemas de partículas')
    director.window.set_location(300, 200)
    director.run(Scene(P1()))


