import tkinter as tk
tk._test()

class Spielfeld:
    def Update():
        pass


class SpielObjekt:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def update(self): 
        pass
    

class Konsumgut(SpielObjekt):
    def update(self):
        pass


class SchlangenGlied(SpielObjekt):
    pass

class SchlangenKopf(SpielObjekt):
    def __init__(self, rotation):
        self.rot = rotation


spielobjekte: list[Spielobjekt] = []


def loop():
    for spielobjekt in spielobjekte:
        spielobjekt.update()


def main(): 
    pass


if __name__ == "__main__": 
    main()