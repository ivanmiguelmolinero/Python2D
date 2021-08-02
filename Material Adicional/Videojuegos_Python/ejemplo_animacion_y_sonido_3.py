
import cocos
from cocos.audio.effect import Effect

class MiCapa(cocos.layer.Layer):

    def __init__(self):
        super().__init__()
        musica_de_fondo = Effect('musica_fondo_retro.wav')
        musica_de_fondo.sound.play()
        musica_de_fondo.sound.fadeout(5000)


if __name__ == '__main__':
    cocos.director.director.init(caption = 'Ejemplo animación y sonido 3',
                                 audio_backend='sdl')
    mi_escena = cocos.scene.Scene(MiCapa())
    cocos.director.director.run(mi_escena)

