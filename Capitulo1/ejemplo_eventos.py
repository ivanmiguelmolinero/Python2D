#-------------------------------------------------------------------------------
# Name:        ejemplo_eventos
# Purpose:
#
# Author:      ivijo
#
# Created:     31/07/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cocos
import pyglet
from cocos.director import director

class EventosTeclado(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super().__init__(64, 200, 255, 255)
        self.texto = cocos.text.Label('', x = 30, y = 10,
                                        font_name = 'arial', font_size = 14)
        self.teclas_pulsadas = set()
        self.actualiza_texto()
        self.add(self.texto)

    def actualiza_texto(self):
        nombres_teclas = [pyglet.window.key.symbol_string(k)
                        for k in self.teclas_pulsadas]
        self.texto.element.text = 'Teclas pulsadas: {}'.format(nombres_teclas)

    def on_key_press(self, key, modifiers):
        self.teclas_pulsadas.add(key)
        self.actualiza_texto()

    def on_key_release(self, key, modifiers):
        self.teclas_pulsadas.discard(key)
        self.actualiza_texto()

class EventosRaton(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()
        self.texto = cocos.text.Label('', font_name = 'arial', font_size = 14,
                                        x = 30, y = 40, color = (100, 0, 100, 255))
        self.add(self.texto)

    def actualiza_texto(self, x, y, texto):
        self.texto.element.text = texto

    def on_mouse_leave(self, x, y):
        self.actualiza_texto(x, y, 'Se ha salido de la ventana')

    def on_mouse_motion(self, x, y, dx, dy):
        self.actualiza_texto(x, y, 'Al moverse las coordenadas '
                            'del ratón son ({},{})'.format(x, y))

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.actualiza_texto(x, y, 'Al arrastrar con el botón {} las coordenadas '
                            'del ratón son ({},{})'.format(buttons, x, y))

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.actualiza_texto(x, y, 'Se ha pulsado el botón número {}'
                            ' del ratón.'.format(buttons))

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y == 1.0:
            self.actualiza_texto(x, y, 'Se ha movido la rueda del ratón '
                                'hacia adelante')
        elif scroll_y == -1.0:
            self.actualiza_texto(x, y, 'Se ha movido la rueda del ratón '
                                'hacia atrás')

class OtrosEventos(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()
        self.texto = cocos.text.Label('', font_name = 'arial', font_size = 14,
                                        x = 30, y = 70, color = (0, 120, 0, 255))
        self.add(self.texto)

    def actualiza_texto(self, x, y, texto):
        self.texto.element.text = texto

    def on_move(self, x, y):
        self.actualiza_texto(x, y, 'Se ha movido la ventana a las '
                            'coordenanadas ({},{})'.format(x, y))

    def on_resize(self, width, heigth):
        self.actualiza_texto(None, None, 'Se ha redimensionado la ventana '
                            'al tamaño {} x {}'.format(width, heigth))


if __name__ == '__main__':
    director.init(resizable = True, caption = 'Ejemplo del manejo de eventos')
    director.run(cocos.scene.Scene(EventosTeclado(), EventosRaton(), OtrosEventos()))
