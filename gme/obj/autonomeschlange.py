from typing import *
from configparser import ConfigParser
import logging

import math


# ----------
# config und logger
# ----------

config = ConfigParser()
config.read("./config.ini")

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

from gme.obj.konsumgut import Konsumgut
from gme.obj.schlange import SchlangenKopf

# ----------


class AutonomerSchlangenKopf(SchlangenKopf):
    def __init__(self, name, spiel, x, y, richtung, laenge, farbe="darkblue", lebensdauer=None):
        super().__init__(name, spiel, x, y, richtung, laenge, farbe, lebensdauer)

        self.name = name

        # links, rechts, oben, unten
        self.richtung = richtung
        self.laenge = laenge

    
    def abstand(self, obj_0, obj_1): 
        return math.sqrt((obj_1.x - obj_0.x)**2 + (obj_1.y - obj_0.y)**2)
    
    def denken(self): 
        moegliche_ziele = [obj for obj in self.spiel.spielobjekte if isinstance(obj, Konsumgut)]
        # ziel ist das naechste Objekt
        ziel = None
        for obj in moegliche_ziele: 
            if self.abstand(obj, self) < self.abstand(ziel, self):
                ziel = obj

        # immer die Achse waehlen, auf welcher dar naechste Apfel am weitesten entfernt ist
        dx, dy = ziel.x - self.x, ziel.y - self.y
        if abs(dx) > abs(dy): 
            if dx > 0: 
                # ziel weiter rechts
                self.richtung = "r"
            else: 
                self.richtung = "l"
        else: 
            if dy > 0:
                # ziel weiter unten
                self.richtung = "u"
            else: 
                self.richtung = "o"

    def aktualisieren(self):
        self.denken()
        super().aktualisieren()
