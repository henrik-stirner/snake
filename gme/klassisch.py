from typing import *
from configparser import ConfigParser
import logging

from random import randint


# ----------
# config und logger
# ----------

config = ConfigParser()
config.read("./config.ini")

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

from gme.obj.schlange import SchlangenKopf, SchlangenGlied
from gme.obj.konsumgut import Apfel

# ----------


class KlassischesSpiel:
    spielobjekte = []

    def __init__(self, spiel_fenster):
        self.spiel_fenster = spiel_fenster

        self.schlange = SchlangenKopf(self, (self.spiel_fenster.w - 1) // 2, (self.spiel_fenster.h - 1) // 2, "o", 2)
        self.apfel = Apfel(self, *self.zufaelliges_freies_feld())

        self.spielobjekte += [self.schlange, self.apfel]

    def aktualisieren(self):
        if self.schlange.tot:
            self.spiel_beenden()

        for spielobjekt in self.spielobjekte:
            if spielobjekt.tot:
                self.spielobjekte.remove(spielobjekt)

        if self.spiel_fenster.eingaben:
            eingabe = self.spiel_fenster.eingaben.pop(0)
            self.eingabe_verarbeiten(eingabe)

        for spielobjekt in self.spielobjekte:
            spielobjekt.aktualisieren()
        self.spielobjekte.sort(key=lambda obj: obj.z_index)
        for spielobjekt in self.spielobjekte:
            spielobjekt.malen()

    def eingabe_verarbeiten(self, eingabe):
        match eingabe:
            case "w":
                self.schlange.richtung = "o"
            case "a":
                self.schlange.richtung = "l"
            case "s":
                self.schlange.richtung = "u"
            case "d":
                self.schlange.richtung = "r"

    def zufaelliges_feld(self):
        x = randint(0, self.spiel_fenster.w-1)
        y = randint(0, self.spiel_fenster.h-1)

        return x, y

    def feld_frei(self, x, y):
        for spielobjekt in self.spielobjekte:
            if x == spielobjekt.x and y == spielobjekt.y:
                return False

        return True

    def objekte_auf_feld(self, x, y):
        objekte_auf_feld = []

        for spielobjekt in self.spielobjekte:
            if x == spielobjekt.x and y == spielobjekt.y:
                objekte_auf_feld.append(spielobjekt)

        return objekte_auf_feld

    def zufaelliges_freies_feld(self):
        x, y = self.zufaelliges_feld()
        # TODO: Was, wenn kein Feld mehr frei ist?
        while not self.feld_frei(x, y):
            x, y = self.zufaelliges_feld()

        return x, y

    def spiel_beenden(self):
        self.spiel_fenster.schliessen()
