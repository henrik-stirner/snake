from typing import *
from configparser import ConfigParser
import logging


# ----------
# config und logger
# ----------

config = ConfigParser()
config.read("./config.ini")

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

from gme.obj.base import SpielObjekt
from gme.obj.konsumgut import Konsumgut

# ----------


class SchlangenGlied(SpielObjekt):
    def __init__(self, spiel, schlangenkopf, lebensdauer):
        super().__init__(spiel, schlangenkopf.x, schlangenkopf.y, "green", 1, lebensdauer)


class SchlangenKopf(SpielObjekt):
    def __init__(self, spiel, x, y, richtung, laenge, lebensdauer=None):
        super().__init__(spiel, x, y, "darkgreen", 2, lebensdauer)

        # links, rechts, oben, unten
        self.richtung = richtung
        self.laenge = laenge

    def aktualisieren(self):
        super().aktualisieren()

        # Konsum
        if spielobjekte := self.spiel.objekte_auf_feld(self.x, self.y):
            for spielobjekt in spielobjekte:
                if isinstance(spielobjekt, Konsumgut):
                    self.laenge += spielobjekt.wertigkeit
                    spielobjekt.konsumiert = True

        # Bombe
        if self.laenge:
            neues_schlangenglied = SchlangenGlied(self.spiel, self, self.laenge)
            self.spiel.spielobjekte.append(neues_schlangenglied)

        # Bewegen: NACH BOMBE UND KONSUM
        match self.richtung:
            case "l":
                if self.x > 0:
                    self.x -= 1
            case "r":
                if self.x < self.spiel.spiel_fenster.w-1:
                    self.x += 1
            case "o":
                if self.y > 0:
                    self.y -= 1
            case "u":
                if self.y < self.spiel.spiel_fenster.h-1:
                    self.y += 1
