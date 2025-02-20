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


class SpielObjekt:
    def __init__(self, spiel, x, y, farbe, lebensdauer=None):
        self.spiel = spiel

        self.x = x
        self.y = y

        self.farbe = farbe

        self.tot = False
        self.lebensdauer: int | None = lebensdauer

    def aktualisieren(self):
        if self.lebensdauer is not None:
            if self.lebensdauer == 0:
                self.farbe = "black"
                self.tot = True
            else:
                self.lebensdauer -= 1

    def malen(self):
        self.spiel.spiel_fenster.kachel_faerben(self.x, self.y, self.farbe)
