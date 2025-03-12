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
    def __init__(self, spiel_fenster, spieler_0_name: str, spieler_1_name: str):
        super().__init__(spiel_fenster)
        self.erlaubte_eingaben +=  config["Steuerung"]["spieler_0"] + config["Steuerung"]["spieler_1"]
        print(self.erlaubte_eingaben)

        self.schlange_0 = SchlangenKopf(spieler_0_name, self, (self.spiel_fenster.w) // 4, (self.spiel_fenster.h) // 2, "o", 2)
        self.schlange_1 = SchlangenKopf(spieler_1_name, self, (self.spiel_fenster.w) // 4 * 3, (self.spiel_fenster.h) // 2, "o", 2)
        self.apfel = Apfel(self, *self.zufaellige_freie_kachel())

        self.spielobjekte += [self.schlange_0, self.schlange_1, self.apfel]

    def aktualisieren(self):
        for spielobjekt in self.spielobjekte:
            if spielobjekt.tot and isinstance(spielobjekt, SchlangenKopf):
                self.spiel_beenden()

        super().aktualisieren()

    def eingabe_verarbeiten(self, eingabe):
        # Richtung: w -> o (oben), a -> l (links), usw.
        i = self.erlaubte_eingaben.index(eingabe)
        if i < 4:
            richtung_0 = "olur"[i]
            self.schlange_0.richtung = richtung_0
        else:
            richtung_1 = "olur"[i-4]
            self.schlange_1.richtung = richtung_1
