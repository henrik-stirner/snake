from typing import *
from configparser import ConfigParser
import logging


# ----------
# config und logger
# ----------

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
        self.erlaubte_eingaben +=  self.config["Steuerung"]["spieler_0"] + self.config["Steuerung"]["spieler_1"]
        self.richtung_eingaben_0 = {
            self.erlaubte_eingaben[0]: (0, -1),     # w -> oben
            self.erlaubte_eingaben[1]: (-1, 0),     # a -> links
            self.erlaubte_eingaben[2]: (0, 1),      # s -> unten
            self.erlaubte_eingaben[3]: (1, 0)       # d -> rechts
        }
        self.richtung_eingaben_1 = {
            self.erlaubte_eingaben[4]: (0, -1),     # i -> oben
            self.erlaubte_eingaben[5]: (-1, 0),     # j -> links
            self.erlaubte_eingaben[6]: (0, 1),      # k -> unten
            self.erlaubte_eingaben[7]: (1, 0)       # l -> rechts
        }

        self.schlange_0 = SchlangenKopf(spieler_0_name, self, (self.spiel_fenster.w) // 4, (self.spiel_fenster.h) // 2, (0, -1), 2)
        self.schlange_1 = SchlangenKopf(spieler_1_name, self, (self.spiel_fenster.w) // 4 * 3, (self.spiel_fenster.h) // 2, (0, -1), 2)
        self.apfel = Apfel(self, *self.zufaellige_freie_kachel())

        self.spielobjekte += [self.schlange_0, self.schlange_1, self.apfel]

    def aktualisieren(self):
        for spielobjekt in self.spielobjekte:
            if spielobjekt.tot and isinstance(spielobjekt, SchlangenKopf):
                self.spiel_beenden()

        super().aktualisieren()

    def eingabe_verarbeiten(self, eingabe):
        # Richtung: w -> o (oben), a -> l (links), usw.
        if eingabe in self.richtung_eingaben_0:
            neue_richtung_0 = self.richtung_eingaben_0[eingabe]
            self.schlange_0.drehen(neue_richtung_0)
        else:
            neue_richtung_1 = self.richtung_eingaben_1[eingabe]
            self.schlange_1.drehen(neue_richtung_1)
