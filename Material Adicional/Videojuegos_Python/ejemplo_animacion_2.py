
import cocos
from pyglet.image import load, ImageGrid

class MiCapa(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()

    def on_mouse_release(self, x, y, buttons, modifiers):
        mi_secuencia = ImageGrid(load('secuencia_explosion.png'), 4, 4)
        mi_animacion = mi_secuencia.get_animation(0.05, loop = False )
        self.mi_sprite = cocos.sprite.Sprite(mi_animacion, (x, y))
        self.add(self.mi_sprite)

if __name__ == '__main__':
    cocos.director.director.init(caption = 'Ejemplo animación 2')
    mi_escena = cocos.scene.Scene(MiCapa())
    cocos.director.director.run(mi_escena)

