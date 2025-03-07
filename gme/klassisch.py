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

from gme.base import Spiel

from gme.obj.schlange import SchlangenKopf
from gme.obj.konsumgut import Apfel

# ----------


class KlassischesSpiel(Spiel):
    def __init__(self, spiel_fenster):
        super().__init__(spiel_fenster)
        self.erlaubte_eingaben += "wasd"

        self.schlange = SchlangenKopf("wasd", self, (self.spiel_fenster.w - 1) // 2, (self.spiel_fenster.h - 1) // 2, "o", 2)
        self.apfel = Apfel(self, *self.zufaellige_freie_kachel())

        self.spielobjekte += [self.schlange, self.apfel]

    def aktualisieren(self):
        for spielobjekt in self.spielobjekte:
            if spielobjekt.tot and isinstance(spielobjekt, SchlangenKopf):
                self.spiel_beenden()

        super().aktualisieren()

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
