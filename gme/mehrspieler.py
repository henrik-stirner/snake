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
    def __init__(self, spiel_fenster, spieler0: str, spieler1: str):
        super().__init__(spiel_fenster)
        self.erlaubte_eingaben += "wasdijkl"

        self.schlange0 = SchlangenKopf(spieler0, self, (self.spiel_fenster.w) // 4, (self.spiel_fenster.h) // 2, "o", 2)
        self.schlange1 = SchlangenKopf(spieler1, self, (self.spiel_fenster.w) // 4 * 3, (self.spiel_fenster.h) // 2, "o", 2)
        self.apfel = Apfel(self, *self.zufaellige_freie_kachel())

        self.spielobjekte += [self.schlange0, self.schlange1, self.apfel]

    def aktualisieren(self):
        for spielobjekt in self.spielobjekte:
            if spielobjekt.tot and isinstance(spielobjekt, SchlangenKopf):
                self.spiel_beenden()

        super().aktualisieren()

    def eingabe_verarbeiten(self, eingabe):
        match eingabe:
            case "w":
                self.schlange0.richtung = "o"
            case "a":
                self.schlange0.richtung = "l"
            case "s":
                self.schlange0.richtung = "u"
            case "d":
                self.schlange0.richtung = "r"

            case "i":
                self.schlange1.richtung = "o"
            case "j":
                self.schlange1.richtung = "l"
            case "k":
                self.schlange1.richtung = "u"
            case "l":
                self.schlange1.richtung = "r"
