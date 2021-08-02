#-------------------------------------------------------------------------------
# Name:        ejemplo_escenas_eventos
# Purpose:
#
# Author:      ivijo
#
# Created:     31/07/2021
# Copyright:   (c) ivijo 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cocos

class VerTexto(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()
        mi_etiqueta = cocos.text.Label('Escena 1',
                                        font_name = 'Consolas',
                                        font_size = 18,
                                        anchor_x = 'center', anchor_y = 'center')

        mi_etiqueta.position = (320, 240)
        self.add(mi_etiqueta)

    def on_mouse_press(self, x, y, buttons, modifiers):
        cocos.director.director.replace(cocos.scene.Scene(VerSprite()))

class VerSprite(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()
        mi_sprite = cocos.sprite.Sprite('mi_ovni_1.png', (320,240))
        self.add(mi_sprite)

    def on_mouse_press(self, x, y, buttons, modifiers):
        cocos.director.director.replace(cocos.scene.Scene(VerTexto()))


if __name__ == '__main__':
    cocos.director.director.init(caption = 'Ejemplo del uso de escenas y eventos')
    cocos.director.director.window.set_location(600, 200)
    escena_1 = cocos.scene.Scene(VerTexto())
    cocos.director.director.run(escena_1)
