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

        self.kopf = schlangenkopf

    def aktualisieren(self):
        if self.kopf.tot:
            self.tot = True

        super().aktualisieren()


class SchlangenKopf(SpielObjekt):
    def __init__(self, name, spiel, x, y, richtung, laenge, lebensdauer=None):
        super().__init__(spiel, x, y, "darkgreen", 2, lebensdauer)

        self.name = name

        # links, rechts, oben, unten
        self.richtung = richtung
        self.laenge = laenge

    def aktualisieren(self):
        # AUSGANGSFELD

        # Konsum
        if spielobjekte := self.spiel.objekte_auf_kachel(self.x, self.y):
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
                self.x -= 1
            case "r":
                self.x += 1
            case "o":
                self.y -= 1
            case "u":
                self.y += 1

        # EIN FELD WEITER

        if not (0 <= self.x <= self.spiel.spiel_fenster.w-1) or not (0 <= self.y <= self.spiel.spiel_fenster.h-1):
            # gegen Wand gefahren
            self.tot = True
        elif any(isinstance(obj, SchlangenGlied) for obj in self.spiel.objekte_auf_kachel(self.x, self.y)):
            # in sich selbst gefahren
            self.tot = True

        super().aktualisieren()
