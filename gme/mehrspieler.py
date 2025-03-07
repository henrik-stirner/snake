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


class MehrspielerSpiel(Spiel):
    erlaubte_eingaben = "wasdijkl"

    def __init__(self, spiel_fenster):
        super().__init__(spiel_fenster)

        self.schlange_wasd = SchlangenKopf("wasd", self, (self.spiel_fenster.w) // 4, (self.spiel_fenster.h) // 2, "o", 2)
        self.schlange_ijkl = SchlangenKopf("ijkl", self, (self.spiel_fenster.w) // 4 * 3, (self.spiel_fenster.h) // 2, "o", 2)
        self.apfel = Apfel(self, *self.zufaellige_freie_kachel())

        self.spielobjekte += [self.schlange_wasd, self.schlange_ijkl, self.apfel]

    def aktualisieren(self):
        for spielobjekt in self.spielobjekte:
            if spielobjekt.tot and isinstance(spielobjekt, SchlangenKopf):
                self.spiel_beenden()

        super().aktualisieren()

    def eingabe_verarbeiten(self, eingabe):
        match eingabe:
            case "w":
                self.schlange_wasd.richtung = "o"
            case "a":
                self.schlange_wasd.richtung = "l"
            case "s":
                self.schlange_wasd.richtung = "u"
            case "d":
                self.schlange_wasd.richtung = "r"

            case "i":
                self.schlange_ijkl.richtung = "o"
            case "j":
                self.schlange_ijkl.richtung = "l"
            case "k":
                self.schlange_ijkl.richtung = "u"
            case "l":
                self.schlange_ijkl.richtung = "r"
