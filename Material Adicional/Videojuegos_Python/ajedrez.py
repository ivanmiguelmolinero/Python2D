
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer
from cocos.sprite import Sprite

class EventosRaton(Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()
        self.agarrado = False
        self.total_piezas = []

        self.tablero = Sprite('tablero_ajedrez.png')
        self.tablero.position=(400,400)
        self.add(self.tablero, z = 0)

        linea = 'TCARYACT'
        paso = (director.window.width - 40) / 8
        x = 20 + paso/2
        for e in linea:
            if e == 'T':
                pieza1 = Sprite('torre_b.png')
                pieza2 = Sprite('torre_n.png')
                pieza3 = Sprite('peon_b.png')
                pieza4 = Sprite('peon_n.png')
            elif e == 'C':
                pieza1 = Sprite('caballo_b.png')
                pieza2 = Sprite('caballo_n.png')
                pieza3 = Sprite('peon_b.png')
                pieza4 = Sprite('peon_n.png')
            elif e == 'A':
                pieza1 = Sprite('alfil_b.png')
                pieza2 = Sprite('alfil_n.png')
                pieza3 = Sprite('peon_b.png')
                pieza4 = Sprite('peon_n.png')
            elif e == 'Y':
                pieza1= Sprite('rey_b.png')
                pieza2 = Sprite('rey_n.png')
                pieza3 = Sprite('peon_b.png')
                pieza4 = Sprite('peon_n.png')
            elif e == 'R':
                pieza1 = Sprite('reina_b.png')
                pieza2 = Sprite('reina_n.png')
                pieza3 = Sprite('peon_b.png')
                pieza4 = Sprite('peon_n.png')

            pieza1.position=(x, 70)
            pieza2.position=(x, 70 + (7*paso-4))
            pieza3.position=(x, 70 + (1*paso-4))
            pieza4.position=(x, 70 + (6*paso-4))

            self.add(pieza1, z=1)
            self.add(pieza2, z=1)
            self.add(pieza3, z=1)
            self.add(pieza4, z=1)

            x += paso

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for elem in self.children:
            if elem[0] == 1 and elem[1].contains(x,y) and not self.agarrado:
                self.agarrado = True
                self.elem_agarrado = elem[1]
        if self.agarrado:
            self.elem_agarrado.position = (x,y)

    def on_mouse_release(self, x, y, buttons, modifiers):
        self.agarrado = False
        for elem in self.children:
            if elem[0] == 1 and elem[1].contains(x,y) and not self.agarrado:
                if elem[1] != self.elem_agarrado:
                    elem[1].kill()


if __name__ == "__main__":
    director.init(width=800, height=800, caption="Ajedrez")
    director.window.set_location(500,100)
    director.run(Scene(EventosRaton()))

