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


class WandlosSpiel(Spiel):
    def __init__(self, spiel_fenster, spieler_name: str):
        super().__init__(spiel_fenster)
        self.erlaubte_eingaben += self.config["Steuerung"]["spieler_0"]
        self.richtung_eingaben = {
            self.erlaubte_eingaben[0]: (0, -1),     # w -> oben
            self.erlaubte_eingaben[1]: (-1, 0),     # a -> links
            self.erlaubte_eingaben[2]: (0, 1),      # s -> unten
            self.erlaubte_eingaben[3]: (1, 0)       # d -> rechts
        }

        self.schlange = SchlangenKopf(spieler_name, self, (self.spiel_fenster.w - 1) // 2, (self.spiel_fenster.h - 1) // 2, (0, -1), 2, wand_teleport=True)
        self.apfel = Apfel(self, *self.zufaellige_freie_kachel())

        self.spielobjekte += [self.schlange, self.apfel]

    def aktualisieren(self):
        for spielobjekt in self.spielobjekte:
            if spielobjekt.tot and isinstance(spielobjekt, SchlangenKopf):
                self.spiel_beenden()

        super().aktualisieren()

    def eingabe_verarbeiten(self, eingabe):
        neue_richtung = self.richtung_eingaben[eingabe]
        self.schlange.drehen(neue_richtung)
