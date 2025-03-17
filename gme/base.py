from typing import *
from configparser import ConfigParser
import logging

from random import randint


# ----------
# config und logger
# ----------

logger = logging.getLogger(__name__)

# ----------
# eigene imports
# ----------

from gme.obj.schlange import Konsumgut
from gme.obj.schlange import SchlangenKopf

# ----------


class Spiel:
    def __init__(self, spiel_fenster):
        self.config = ConfigParser()
        self.config.read("./config.ini")

        self.delay = self.config["Spiel"]["delay"]

        self.erlaubte_eingaben = ""
        self.spielobjekte = []

        self.spiel_fenster = spiel_fenster

    def aktualisieren(self):
        for spielobjekt in self.spielobjekte:
            if spielobjekt.tot and not isinstance(spielobjekt, SchlangenKopf):
                self.spielobjekte.remove(spielobjekt)

        if self.spiel_fenster.eingaben:
            eingabe = self.spiel_fenster.eingaben.pop(0)
            self.eingabe_verarbeiten(eingabe)

        for spielobjekt in self.spielobjekte:
            spielobjekt.aktualisieren()
        self.spielobjekte.sort(key=lambda obj: obj.z_index)
        for spielobjekt in self.spielobjekte:
            spielobjekt.malen()

    def eingabe_verarbeiten(self, eingabe):
        pass

    def zufaellige_kachel(self):
        x = randint(0, self.spiel_fenster.w-1)
        y = randint(0, self.spiel_fenster.h-1)

        return x, y

    def kachel_frei(self, x, y):
        for spielobjekt in self.spielobjekte:
            if x == spielobjekt.x and y == spielobjekt.y:
                return False

        return True

    def objekte_auf_kachel(self, x, y):
        objekte = []

        for spielobjekt in self.spielobjekte:
            if x == spielobjekt.x and y == spielobjekt.y:
                objekte.append(spielobjekt)

        return objekte

    def instanz_auf_kachel(self, x, y, typ: Type):
        return any([isinstance(obj, typ) for obj in self.objekte_auf_kachel(x, y)])

    def kachel_begehbar(self, x, y):
        if not ((0 <= x <= self.spiel_fenster.w - 1) and (0 <= y <= self.spiel_fenster.h - 1)):
            # nicht auf Spielfeld
            return False

        if not all([isinstance(obj, Konsumgut) for obj in self.objekte_auf_kachel(x, y)]):
            return False

        return True

    def zufaellige_freie_kachel(self):
        x, y = self.zufaellige_kachel()
        # TODO: Was, wenn kein Feld mehr frei ist?
        while not self.kachel_frei(x, y):
            x, y = self.zufaellige_kachel()

        return x, y

    def spiel_beenden(self):
        self.spiel_fenster.schliessen()
