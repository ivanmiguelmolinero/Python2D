
import cocos
from cocos.audio.effect import Effect
from pyglet.image import load, ImageGrid, Animation

class MiCapa(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()
        global musica_de_fondo
        musica_de_fondo = Effect('musica_fondo_retro.wav')
        musica_de_fondo.sound.set_volume(0.1)
        musica_de_fondo.sound.play(-1)

    def on_mouse_release(self, x, y, buttons, modifiers):
        sonido_explosion = Effect('explosion.wav')
        sonido_explosion.sound.set_volume(0.1)
        sonido_explosion.sound.play()
        mi_secuencia = ImageGrid(load('secuencia_explosion.png'), 4, 4)
        mi_animacion = Animation.from_image_sequence(mi_secuencia, 0.05, False)
        self.mi_sprite = cocos.sprite.Sprite(mi_animacion, (x, y))
        self.add(self.mi_sprite)


def cierra_ventana():
    musica_de_fondo.sound.stop()
    cocos.director.director.window.close()


if __name__ == '__main__':
    cocos.director.director.init(caption = 'Ejemplo animación y sonido 2',
                                 audio_backend='sdl')
    mi_escena = cocos.scene.Scene(MiCapa())
    cocos.director.director.window.on_close = cierra_ventana
    cocos.director.director.run(mi_escena)

