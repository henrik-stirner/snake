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
from gme.obj.autonomeschlange import AutonomerSchlangenKopf
from gme.obj.konsumgut import Apfel

# ----------


class SimulationSpiel(Spiel):
    def __init__(self, spiel_fenster):
        super().__init__(spiel_fenster)
        self.autonome_schlange_0 = AutonomerSchlangenKopf(self, (self.spiel_fenster.w - 1) // 4, (self.spiel_fenster.h - 1) // 2, (0, -1), 2)
        self.autonome_schlange_1 = AutonomerSchlangenKopf(self, (self.spiel_fenster.w - 1) // 4 * 3, (self.spiel_fenster.h - 1) // 2, (0, -1), 2)
        self.apfel = Apfel(self, *self.zufaellige_freie_kachel())

        self.spielobjekte += [self.autonome_schlange_0, self.autonome_schlange_1, self.apfel]

    def aktualisieren(self):
        for spielobjekt in self.spielobjekte:
            if spielobjekt.tot and isinstance(spielobjekt, SchlangenKopf):
                self.spiel_beenden()

        super().aktualisieren()
