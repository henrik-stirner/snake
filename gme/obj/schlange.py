from typing import *
from configparser import ConfigParser
import logging

from gme.obj.base import SpielObjekt


# ----------
# config und logger
# ----------


config = ConfigParser()
config.read("./config.ini")

logger = logging.getLogger(__name__)


# ----------


class SchlangenGlied(SpielObjekt):
    def __init__(self, spiel, schlangenkopf, lebensdauer):
        super().__init__(spiel, schlangenkopf.x, schlangenkopf.y, "green", lebensdauer=lebensdauer)


class SchlangenKopf(SpielObjekt):
    def __init__(self, spiel, x, y, richtung, laenge):
        super().__init__(spiel, x, y, "darkgreen")

        # links, rechts, oben, unten
        self.richtung = richtung
        self.laenge = laenge

    def aktualisieren(self):
        super().aktualisieren()

        if self.laenge:
            neues_schlangenglied = SchlangenGlied(self.spiel, self, self.laenge)
            self.spiel.spielobjekte.append(neues_schlangenglied)

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

        # TODO: Kollisionen -> Apfel "essen"
