
def f1():
    a = 1
    var_locales = locals()
    print("Variables locales antes de ejecutar exec() y tras ejecutar locals(): ", var_locales)
    exec("b = a + 4\na += 1")
    print("Variables locales después de ejecutar exec(): ", var_locales)
    locals()
    print("Variables locales después de ejecutar de nuevo locals(): ", var_locales)

def f2():
    a = 1
    var_locales = locals()
    print("Variables locales antes de ejecutar exec(): ", var_locales)
    exec("b = a + 4\na += 1", {}, var_locales)
    print("Variables locales después de ejecutar exec(): ", var_locales)
    locals()
    print("Variables locales después de ejecutar de nuevo locals(): ", var_locales)

def f3():
    a = 1
    mis_loc = {'a': a}
    print("Mis variables locales antes de ejecutar exec(): ", mis_loc)
    exec("b = a + 4\na += 1", {}, mis_loc)
    print("Mis variables locales después de ejecutar exec(): ", mis_loc)
    locals()
    print("Mis variables locales después de ejecutar locals(): ", mis_loc)


print("f1()" + 92*'-')
f1()
print("\nf2()" + 92*'-')
f2()
print("\nf3()" + 92*'-')
f3()
