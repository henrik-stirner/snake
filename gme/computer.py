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
from gme.obj.autonomeschlange import AutonomerSchlangenKopf
from gme.obj.konsumgut import Apfel

# ----------


class ComputerSpiel(Spiel):
    def __init__(self, spiel_fenster, spieler_name: str):
        super().__init__(spiel_fenster)
        self.erlaubte_eingaben += config["Steuerung"]["spieler_0"]

        self.schlange = SchlangenKopf(spieler_name, self, (self.spiel_fenster.w - 1) // 2, (self.spiel_fenster.h - 1) // 2, "o", 2)
        self.autonome_schlange = AutonomerSchlangenKopf()
        self.apfel = Apfel(self, *self.zufaellige_freie_kachel())

        self.spielobjekte += [self.schlange, self.apfel]

    def aktualisieren(self):
        for spielobjekt in self.spielobjekte:
            if spielobjekt.tot and isinstance(spielobjekt, SchlangenKopf):
                self.spiel_beenden()

        super().aktualisieren()

    def eingabe_verarbeiten(self, eingabe):
        # Richtung: w -> o (oben), a -> l (links), usw.
        richtung = "olur"[self.erlaubte_eingaben.index(eingabe)]
        self.schlange.richtung = richtung
