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
    def __init__(self, spiel_fenster, spieler0: str):
        super().__init__(spiel_fenster)
        self.erlaubte_eingaben += config["Steuerung"]["spieler0"]

        self.schlange0 = SchlangenKopf(spieler0, self, (self.spiel_fenster.w - 1) // 2, (self.spiel_fenster.h - 1) // 2, "o", 2)
        self.apfel = Apfel(self, *self.zufaellige_freie_kachel())

        self.spielobjekte += [self.schlange0, self.apfel]

    def aktualisieren(self):
        for spielobjekt in self.spielobjekte:
            if spielobjekt.tot and isinstance(spielobjekt, SchlangenKopf):
                self.spiel_beenden()

        super().aktualisieren()

    def eingabe_verarbeiten(self, eingabe):
        # Richtung: w -> o (oben), a -> l (links), usw.
        richtung0 = "olur"[self.erlaubte_eingaben.index(eingabe)]
        self.schlange0.richtung= richtung0
