
from functools import partial

def mi_funcion(x,y,z=10):
    print(x+y+z)

def mi_funcion2(*args, **kwargs):
    print(args, kwargs)

p1 = partial(mi_funcion, 1,5)
p2 = partial(mi_funcion, 1,5,20)
p3 = partial(mi_funcion, 2,10,z=100)
p1()
p2()
p3()

p4 = partial(mi_funcion2, 1,2,3,4,5,6, t=25)
p4()
