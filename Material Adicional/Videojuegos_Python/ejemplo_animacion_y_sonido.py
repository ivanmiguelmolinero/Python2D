
import cocos
from cocos.audio.effect import Effect
from pyglet.image import load, ImageGrid, Animation

class MiCapa(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()

    def on_mouse_release(self, x, y, buttons, modifiers):
        mi_efecto_sonoro = Effect('explosion.wav')
        mi_efecto_sonoro.sound.set_volume(0.1)
        mi_efecto_sonoro.play()
        mi_secuencia = ImageGrid(load('secuencia_explosion.png'), 4, 4)
        mi_animacion = Animation.from_image_sequence(mi_secuencia, 0.05, False)
        self.mi_sprite = cocos.sprite.Sprite(mi_animacion, (x, y))
        self.add(self.mi_sprite)


if __name__ == '__main__':
    cocos.director.director.init(caption = 'Ejemplo animación y sonido',
                                 audio_backend='sdl')
    mi_escena = cocos.scene.Scene(MiCapa())
    cocos.director.director.run(mi_escena)

