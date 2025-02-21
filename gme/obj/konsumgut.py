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

from gme.obj.base import SpielObjekt

# ----------


class Konsumgut(SpielObjekt):
    def __init__(self, spiel, x, y, farbe, wertigkeit):
        super().__init__(spiel, x, y, farbe)

        self.aktive_farbe = farbe
        self.konsumiert = False
        self.wertigkeit = wertigkeit

    def malen(self):
        self.farbe = self.aktive_farbe if not self.konsumiert else "black"

        super().malen()


class Apfel(Konsumgut):
    def __init__(self, spiel, x, y):
        super().__init__(spiel, x, y, "red", 1)

    def aktualisieren(self):
        if self.konsumiert:
            self.x, self.y = self.spiel.zufaelliges_freies_feld()
            self.konsumiert = False
