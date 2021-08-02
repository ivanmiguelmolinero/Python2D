
from cocos.tiles import load
from cocos.layer import ScrollingManager
from cocos.director import director
from cocos.scene import Scene

if __name__ == '__main__':
    ventana = director.init(width=384, height=384, caption="Cargar tile map")
    ventana.set_location(600, 200)

    mi_mapa = load("mapa1.tmx")["capa0"]

    manejador_scroll = ScrollingManager()
    manejador_scroll.add(mi_mapa)

    director.run(Scene(manejador_scroll))

