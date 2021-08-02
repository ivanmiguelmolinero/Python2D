
import cocos
from cocos.scenes.transitions import FadeTransition

class VerTexto(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        mi_etiqueta = cocos.text.Label('Escena 1',
                                       font_name = 'Consolas',
                                       font_size = 18,
                                       anchor_x = 'center', anchor_y = 'center')
        mi_etiqueta.position = (320, 240)
        self.add(mi_etiqueta)


class VerTexto2(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        mi_etiqueta = cocos.text.Label('Escena 2',
                                       font_name = 'Consolas',
                                       font_size = 18,
                                       anchor_x = 'center', anchor_y = 'center')
        mi_etiqueta.position = (320, 240)
        self.add(mi_etiqueta)


if __name__ == "__main__":
    cocos.director.director.init(caption= 'Sencilla transición entre escenas')

    escena_1 = cocos.scene.Scene(VerTexto())
    escena_2 = cocos.scene.Scene(VerTexto2())

    cocos.director.director.run(FadeTransition(escena_2, 5, escena_1))

