
import cocos

class VerTexto(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        mi_etiqueta = cocos.text.Label('Visualización de un texto simple',
                                       font_name = 'Consolas',
                                       font_size = 18,
                                       anchor_x = 'center', anchor_y = 'center')

        mi_etiqueta.position = (320, 240)
        self.add(mi_etiqueta)

if __name__ == "__main__":
    cocos.director.director.init(caption = 'Ejemplo sencillo 1')
    capa_texto = VerTexto()
    escena_principal = cocos.scene.Scene(capa_texto)
    cocos.director.director.run(escena_principal)

